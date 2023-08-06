import argparse
from datetime import datetime
import csv
import json
from pathlib import Path
import pandas as pd

import PyLab.vars


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1', 'on'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0', 'off'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def filename_formatter(path, metadata={}):

    dt = datetime.now()
    path_with_date = dt.strftime(path)
    path_with_date_metadata = path_with_date.format(**metadata)
    return path_with_date_metadata


def filename_append_timestamp(path):
    dt = datetime.now()
    append_path_date = dt.strftime("_%Y%m%d_%H%M%S")

    suffix = Path(path).suffix
    new_path = path[:(-1)*len(suffix)] + append_path_date + suffix
    return new_path


def dict_with_prefix(dict, prefix):
    result = {}
    for key, value in dict.items():
        result[prefix + key] = value
    return result


out_df = pd.DataFrame()
compact_out_df = pd.DataFrame()
_df = pd.DataFrame()


def save_meas_json_to_file(data, path):
    # save meas json to csv or json format
    if path[-4:] == ".csv":
        with open(path, 'w', newline='') as csv_file:
            file = csv.writer(csv_file)
            if "metadata" in data:
                for key, value in data["metadata"].items():
                    file.writerow([key, value])
                file.writerow([])
                file.writerow([])

            if len(data["data"]) > 0:
                file.writerow(data["data"][0].keys())
                for dat in data["data"]:
                    file.writerow(dat.values())

    else:
        with open(path, 'w') as file:
            file.write(json.dumps(data, indent=4))

    # if output data in one file
    if pylab.vars.output_data_file_path:
        global out_df, compact_out_df, _df

        # prefix, add channel if exists
        if data["metadata"]["channel"]:
            prefix = f"""{data["metadata"]["device_type"]}_{data["metadata"]["channel"]}_{data["metadata"]["mode"]}_mean_"""
        else:
            prefix = f"""{data["metadata"]["device_type"]}_{data["metadata"]["mode"]}_mean_"""

        # Append one more row of data
        df = pd.DataFrame.from_dict([dict(dict_with_prefix(item, prefix), **dict_with_prefix(data["metadata"], "metadata_"),
                                    **dict_with_prefix(pylab.vars.loop_variables, "loop_")) for item in data["data"]])

        out_df = pd.concat([out_df, df])

        out_df.to_csv(pylab.vars.output_data_file_path, index=False)

        # Compact one more row of data
        # get mean value of measurements
        df_without_meta = pd.DataFrame.from_dict([dict(dict_with_prefix({
            "timestamp": item["timestamp"],
            "value":item["value"]
        }, prefix),
            **dict_with_prefix(pylab.vars.loop_variables, "loop_")) for item in data["data"]]).mean().to_frame().T

        # merge with same loop variables or concate data frames
        if [col for col in _df if col.startswith("loop")] == [col for col in df_without_meta if col.startswith("loop")] and [_df[col].item() for col in _df if col.startswith("loop")] == [df_without_meta[col].item() for col in df_without_meta if col.startswith("loop")]:
            if not _df.empty:
                # merge if _df not empty
                _df = pd.merge(df_without_meta, _df, how="right")
            else:
                # give initial value to _df
                _df = df_without_meta

        else:
            # concat dataframes
            compact_out_df = pd.concat([compact_out_df, _df])
            _df = df_without_meta

        # write to file
        compact_out_df.to_csv(
            pylab.vars.output_data_file_path[:-4] + "_compact.csv", index=False)
