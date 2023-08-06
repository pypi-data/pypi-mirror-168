import argparse
from datetime import datetime

# current datetime
dt = datetime.now()

# argparser for command line.
main_parser = argparse.ArgumentParser(
    description='PyLab for multimeter, oscilloscope and more.')
main_parser.add_argument('--log-file', type=str, default='logging.ini',
                         help='Logger configuration file location.')
main_parser.add_argument('--log-level', type=str,
                         default='INFO', help='Log level',
                         choices=["CRITICAL", "ERROR", "WARNING",  "INFO", "DEBUG",  "NOTSET"])
main_parser.add_argument('-f', '--file', type=str,
                         help='Command file')
main_parser.add_argument('--data-file', type=str, default=dt.strftime('./data/pylab_run_%Y%m%d_%H%M%S.csv'),
                         help='output file locationfor all data in csv')


def get_console_args() -> argparse.Namespace:
    """
    Get the console arguments

    Returns:
        Arguments

    Raises:
        KeyError: Cannot find keys in logging_config_file
        AssertionError: log_level not supported 
    """
    args = main_parser.parse_args()
    return args
