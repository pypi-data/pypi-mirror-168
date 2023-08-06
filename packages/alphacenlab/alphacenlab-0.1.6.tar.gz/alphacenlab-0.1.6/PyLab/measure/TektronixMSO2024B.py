from cProfile import label
from .SCPIDevice import SCPIDevice
from .utils import filename_formatter, filename_append_timestamp, save_meas_json_to_file, str2bool
import traceback
import time
import logging
import numpy as np
import matplotlib.pyplot as pl

logger = logging.getLogger()

def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

class TekSCPIDevice(SCPIDevice):
    """
    TekSCPIDevice do not support :SYSTEM:ERROR?, ignoring 
    """
    @property
    def err(self):
        return [0]


class TektronixMSO2024B(TekSCPIDevice):
    """
    Deivce Tektronix MSO2024B command
    """
    # constants
    resolutions = ["REDUCED", "FULL"]
    channels = ["CH1", "CH2", "CH3", "CH4"]
    maths = ["MATH"]
    refs = ["REF1", "REF2"]
    buses = ["BUS:B1", "BUS:B2"]
    digital_channels = [f"D{x}" for x in range(16)]  # 16 channels in total
    measurement_modes = ["AMP", "AREA", "BURST", "CAREA", "CMEAN", "CRMS", "DELAY", "FALL", "FREQ", "HIGH", "LOW", "MAX", "MEAN", "MIN",
                         "NDUTY", "NEDGECOUNT", "NOVERSHOOT", "NPULSECOUNT", "NWIDTH", "PEDGECOUNT", "PDUTY", "PERIOD", "PHASE", "PK2PK", "POVERSHOOT", "PPULSECOUNT", "PWIDTH", "RISE", "RMS"]
    trigger_modes = ["AUTO", "NORMAL"]
    trigger_types = ["EDGE", "LOGIC", "PULSE", "BUS", "VIDEO"]
    trigger_slopes = ["FALL", "RISE"]
    gatings = ["OFF", "SCREEN", "CURSORS"]
    acquire_stop_afters = ["RUNST", "SEQ"]  # Runstop and sequence

    def __init__(self, scpiHandle, device_alias: str = None):
        super(TektronixMSO2024B, self).__init__(scpiHandle)
        self.device_alias = device_alias

    def __del__(self):
        self.inst.close()

    @property
    def metadata(self):
        return {
            "device_type": self.__class__.__name__,
            "resource_name": self.inst.resource_name,
            "start_time": None,
            "end_time": None,
            "resolution": None,
            "channel": None,
        }
    def reset(self):
        self.inst.timeout = 10000 # ms
        self.inst.encoding = 'latin_1'
        self.inst.read_termination = '\n'
        self.inst.write_termination = None
        self.inst.write('*cls') # clear ESR


        self.inst.write('*rst') # reset
        r = self.inst.query('*opc?') # sync

        self.inst.write('autoset EXECUTE') # autoset
        r = self.inst.query('*opc?') # sync

    def get_single_waveform(self,channel=1):
        """
        get one channel waveform from osc

        Arg:
            channel - specify the channel # to read

        Return:
            wav - 1d array scaled waveform without time info
        
        """
        # io config
        self.inst.write(f'data:source CH{channel}') # channel

        r = self.inst.query('*opc?') # sync

        # data query
        bin_wave = self.inst.query_binary_values('curve?', datatype='b', container=np.array)

        # retrieve scaling factors
        vscale = float(self.inst.query('wfmpre:ymult?')) # volts / level
        voff = float(self.inst.query('wfmpre:yzero?')) # reference voltage
        vpos = float(self.inst.query('wfmpre:yoff?')) # reference position (level)

        # error checking
        # r = int(self.inst.query('*esr?'))
        # r = self.inst.query('allev?').strip()

        # create scaled vectors
        # vertical (voltage)
        unscaled_wave = np.array(bin_wave, dtype='double') # data type conversion
        scaled_wave = (unscaled_wave - vpos) * vscale + voff

        return scaled_wave

    def get_time_series(self):
        """
        get time series from osc

        Arg:
            None

        Return:
            time series - 1d array times series to match wvf
        
        """
        # # of samples of 1 waveform on screen
        record = int(self.inst.query('wfmpre:nr_pt?'))

        # horizontal (time)
        tscale = float(self.inst.query('wfmpre:xincr?'))
        tstart = float(self.inst.query('wfmpre:xzero?'))

        total_time = tscale * record
        tstop = tstart + total_time
        scaled_time = np.linspace(tstart, tstop, num=record, endpoint=False)

        return record, scaled_time



    def set_acquire(self,resolution = 'reduced'):
        """
        show wfm plot 

        Arg:
            channels - all the interested channel # in a list
            resolution - reduced or full
            smooth factor - remove the noise smooth_factor=1 as no smooth applied
        Return:
            None for now
        
        """
        self.inst.write('acquire:state 0') # stop
        self.inst.write('acquire:stopafter SEQUENCE') # single
        self.inst.write('acquire:state 1') # run
        self.inst.write('data:resolution '+resolution)
        record, scaled_time = self.get_time_series()

        self.inst.write('header 0')
        self.inst.write('data:encdg RIBINARY')
        self.inst.write('data:start 1') # first sample
        self.inst.write('data:stop {}'.format(record)) # recordlast sample
        self.inst.write('wfmpre:byt_nr 1') # 1 byte per sample

    def set_filterVu(self):
        freq_str = self.inst.query(f"FILTERVu:FREQuency:AVAILable?")
        r = self.inst.query('*opc?') # sync
        freq = str.split(freq_str.strip("/n"), ",")
        freq_num = []
        for i in freq:
            freq_num.append(int(i))
        self.inst.write(f"FILTERVu:FREQuency {min(freq_num)}")
        r = self.inst.query('*opc?') # 
        print("filtered at : ", min(freq_num))

    def save_waveform(self, filename="./data/MSO.csv", resolution="REDUCED", gating="SCREEN"):
        """
        Save MSO ALL waveforms into csv

        Args:
            filename: filename to save, end with csv, support replacing `metadata` and python `datetime` `strftime` method
            resolution: ["REDUCED", "FULL"] 
                REDUCED (Default) gives reduced waveform data, takes a short time, ~10s
                FULL gives FULL waveform data, >30s
            gating: ["OFF","SCREEN","CURSORS"]
                SCREEN (default) save waveform shown on the screen
                OFF save FULL range of waveform
                CURSORS save waveform between cursors

        Retuns:
            None
        """

        resolution = resolution.upper()
        assert resolution in self.resolutions
        gating = gating.upper()
        assert gating in self.gatings

        start_time = time.time()

        # change resolution
        if resolution == "REDUCED":
            self.inst.write(f"SAVE:WAVEFORM:SPREADSheet:RESOLution REDUced")
        elif resolution == "FULL":
            self.inst.write(f"SAVE:WAVEFORM:SPREADSheet:RESOLution FULL")
        self.inst.query('*OPC?')

        # Change gating
        self.inst.write(f"SAVe:WAVEform:GATIng {gating}")

        # set a long timeout to prevent error
        self.inst.timeout = 1000*1000

        # save CSV data
        self.inst.write(f"SAVE:WAVEFORM ALL,\"E:/TEMP.CSV\"")

        # until operation complete
        self.inst.query('*OPC?')

        # reset timeout
        self.inst.timeout = 10*1000

        # read waveform csv
        self.inst.write('FILESystem:READFile \"E:/TEMP.CSV\"')
        waveform_data = self.inst.read_raw(1024*1024*1024)
        end_time = time.time()

        metadata = {
            **self.metadata,
            "start_time": start_time,
            "end_time": end_time,
            "resolution": resolution,
            "channel": "ALL"
        }

        # Save image data to local disk
        with open(filename_formatter(filename, metadata), "wb", buffering=0) as file:
            file.write(waveform_data)

        return None

    def save_img(self, filename="./data/MSO.bmp") -> None:
        """
        Save MSO screen image 

        Args:
            filename: filename to save, end with bmp

        Retuns:
            None

        """
        start_time = time.time()
        # Save BMP format file
        self.write('SAVe:IMAGe:FILEFormat BMP')

        # Save image to instrument's local disk
        self.write('SAVE:IMAGe \"E:/Temp.bmp\"')

        # Wait for instrument to finish writing image to disk
        self.query('*OPC?')

        # Read image file from instrument
        self.inst.write('FILESystem:READFile \"E:/Temp.bmp\"')
        img_data = self.inst.read_raw(1024*1024)
        end_time = time.time()

        # Save image data to local disk
        metadata = {
            **self.metadata,
            "start_time": start_time,
            "end_time": end_time,
        }
        with open(filename_formatter(filename, metadata), "wb", buffering=0) as file:
            file.write(img_data)

    def set_label(self, channel: str, label: str):
        """
        Set MSO channel label

        Args:
            channel: suppport channels (CH1,...), maths (MATH), refs (REF1,...), buses (BUS:B1,...), digitial channels (D0,D1...)
            label: label display on MSO

        Return:
            None 
        """
        assert channel in [*self.channels, *
                           self.maths, *self.refs, *self.buses, *self.digital_channels]
        self.write(f"""{channel}:LABel "{label}" """)

    def measure(self, channel, mode, times: int, interval: float, measurement_source=1, filename=None):
        """
        MSO measurement

        Args:
            channel: suppport channels (CH1,...), maths (MATH), 
            mode: MSO measuring mode. For all modes and details, please refer to MSO docs
            times: number of mesaurements
            interval: time interval between two measurement, in seconds
            measurement_source: defualt 1, MSO measurement source
            filename: None for not saving, otherwise save to csv format if ends with csv or json format.

        Returns:
            dict
            {
                "metadata": {
                    "start_time": start_time,
                    "end_time": end_time,
                    "device_type": self.__class__.__name__,
                    "resource_name": self.inst.resource_name,
                    "mode": mode,
                    "unit": unit
                },
                "data": [
                    {
                        "timestamp": timestamp,
                        "index": i,
                        "value": value
                    },
                    ...
                ]
            }
        """
        assert channel in [*self.channels, *self.maths]
        assert mode in self.measurement_modes

        self.write(f"MEASUrement:MEAS:SOUrce{measurement_source} {channel}")

        self.write(f"MEASUrement:MEAS:TYPe {mode}")

        value = self.query("MEASUrement:MEAS:VALue?")
        unit = self.query("MEASUrement:MEAS:UNIts?").replace('"', "").strip()

        start_time = time.time()
        data = []
        for i in range(times):
            value = self.get_val()
            timestamp = time.time()
            logger.info(f"{str(timestamp)}, {value}")
            data.append({
                "timestamp": timestamp,
                "index": i,
                "value": value
            })
            if i != (times-1):
                time.sleep(interval)
        end_time = time.time()
        result = {
            "metadata": {
                "start_time": start_time,
                "end_time": end_time,
                "device_type": self.__class__.__name__,
                "resource_name": self.inst.resource_name,
                "mode": mode,
                "unit": str(unit),
                "channel": channel
            },
            "data": data
        }

        if filename:
            save_meas_json_to_file(result, filename_formatter(filename))
        return result

    def get_val(self) -> float:
        """
        Get measurement value

        Returns:
            float: measurement result
        """
        # Difference between MEASUrement:MEAS:VALue? MEASUrement:IMMed:VALue?
        # MEASUrement:MEAS:VALue? This is the same value as displayed on-screen. If measurement statisticsare enabled, a new value is calculated with every waveform. In addition, thisvalue is updated approximately every 1/3 second. If you are acquiring a longacquisition record, the oscilloscope may take longer to update.
        # MEASUrement:IMMed:VALue? Returns the value of the measurement specified by theMEASUrement:IMMed:TYPe command. The measurement is immediately taken on the source(s)specified by a MEASUrement:IMMed:SOUrce1 command.
        # MEASUrement:IMMed:VALue? may takes longer time as it need to trigger again.
        value = self.query("MEASUrement:MEAS:VALue?")
        return float(value)

    def get_unit(self) -> str:
        """
        Get measurement unit

        Returns:
            string: measurement unit
        """
        value = self.query("MEASUrement:MEAS:UNIts?").replace('"', "").strip()
        return str(value)

    def set_measurement_mode(self, channel, mode, measurement_source=1,) -> None:
        """
        MSO measurement

        Args:
            channel: suppport channels (CH1,...), maths (MATH), 
            mode: MSO measuring mode. For all modes and details, please refer to MSO docs

        Returns:
            None
        """
        assert channel in [*self.channels, *self.maths]
        assert mode in self.measurement_modes

        self.write(f"MEASUrement:MEAS:SOUrce{measurement_source} {channel}")

        self.write(f"MEASUrement:MEAS:TYPe {mode}")

    @property
    def horizontal_scale(self) -> float:
        """
        Get horizontal scale

        Returns:
            float: horizontal scale
        """
        scale = self.query("HORizontal:SCAle?")
        return float(scale)

    @horizontal_scale.setter
    def horizontal_scale(self, scale) -> None:
        """
        Set horizontal scale from 2 ns to 100 s, depending on the oscilloscope model. 

        Args:
            scale: float in seconds

        Returns:
            None
        """
        self.write(f"HORizontal:SCAle {scale}")
        logger.info(f"Horizontal scale is {self.horizontal_scale}")

    def set_gain(self, channel, gain) -> None:
        """
        The "gain" of a probe is the output divided by the input transfer ratio. For example, a common 10x probe has a gain of 0.1.

        Args:
            channel: channel id
            gain: float. Gain value

        Returns:
            None
        """
        assert channel in [*self.channels]
        self.write(f"{channel}:PRObe:GAIN {gain}")
        try:
            device_gain = self.get_gain(channel)
            assert gain == device_gain
            logger.info(f"Gain on device: {device_gain}")
        except AssertionError:
            logger.warn(
                f"Gain not match! input: {gain} device: {device_gain} ")

    def get_gain(self, channel) -> float:
        """
        The "gain" of a probe is the output divided by the input transfer ratio. For example, a common 10x probe has a gain of 0.1.

        Args:
            channel: id

        Returns:
            float
        """
        assert channel in [*self.channels]
        value = self.query(f"{channel}:PRObe:GAIN?")

        return float(value)

    def _vertical_channel(self, channel) -> str:
        """
        vertical channel prefix

        Args:
            Channel: Channel id
        Returns:
            str, appends :VERTical: to channel if it's refs or maths
        """
        if channel in self.channels:
            return channel
        elif channel in [*self.refs, *self.maths]:
            return f"{channel}:VERTical:"

    def set_offset(self, channel, offset: float) -> None:
        """
        Offset adjusts only the vertical center of the acquisition window for channel waveforms to help determine what data is acquired. The oscilloscope always displays the input signal minus the offset value.

        Args:
            channel: channel id
            offset: float

        Returns:
            None
        """
        assert channel in [*self.channels, *self.refs, *self.maths]
        self.write(f"{self._vertical_channel(channel)}:OFFSet {offset}")
        try:
            device_offset = self.get_offset(channel)
            assert offset == device_offset
            logger.info(f"Offset on device: {device_offset}")
        except AssertionError:
            logger.warn(
                f"Offset not match! input: {offset} device: {device_offset} ")

    def get_offset(self, channel):
        """
        Offset adjusts only the vertical center of the acquisition window for channel waveforms to help determine what data is acquired. The oscilloscope always displays the input signal minus the offset value.

        Args:
            channel: channel id

        Returns:
            float: offset
        """
        assert channel in [*self.channels, *self.refs, *self.maths]

        value = self.query(f"{self._vertical_channel(channel)}:OFFSet?")

        return float(value)

    def set_position(self, channel, position: float) -> None:
        """
        Set channel position in volts
        The position value determines the vertical graticule coordinate at which input signal values, minus the present offset setting for that channel, are displayed. For example, if the position for Channel 3 is set to 2.0 and the offset is set to 3.0, then input signals equal to 3.0 units are displayed 2.0 divisions above the center of the screen (at 1 V/div).

        Args:
            channel: channel id
            position: float

        Returns: None
        """
        assert channel in [*self.channels, *self.refs,
                           *self.maths, *self.digital_channels]
        self.write(f"{self._vertical_channel(channel)}:POSition {position}")
        try:
            device_position = self.get_position(channel)
            assert position == device_position
            logger.info(f"position on device: {device_position}")
        except AssertionError:
            logger.warn(
                f"position not match! input: {position} device: {device_position} ")

    def get_position(self, channel) -> float:
        """
        Get channel position in volts

        Args:
            channel: channel id

        Returns:
            float: channel id
        """
        assert channel in [*self.channels, *self.refs,
                           *self.maths, *self.digital_channels]

        value = self.query(f"{self._vertical_channel(channel)}:POSition?")

        return float(value)

    def set_scale(self, channel, scale: float) -> None:
        """
        Each waveform has a vertical scale parameter. For a signal with constant amplitude, increasing the Scale causes the waveform to be displayed smaller. Decreasing the scale causes the waveform to be displayed larger.

        Args:
            channel: channel id
            scale: float.

        Returns:
            None
        """
        assert channel in [*self.channels, *self.refs, *self.maths]
        self.write(f"{self._vertical_channel(channel)}:SCAle {scale}")
        try:
            device_scale = self.get_scale(channel)
            assert scale == device_scale
            logger.info(f"scale on device: {device_scale}")
        except AssertionError:
            logger.warn(
                f"scale not match! input: {scale} device: {device_scale} ")

    def get_scale(self, channel):
        """
        Each waveform has a vertical scale parameter. For a signal with constant amplitude, increasing the Scale causes the waveform to be displayed smaller. Decreasing the scale causes the waveform to be displayed larger.

        Args:
            channel: channel id

        Returns:
            scale: float.
        """
        assert channel in [*self.channels, *self.refs, *self.maths]

        value = self.query(f"{self._vertical_channel(channel)}:SCAle?")

        return float(value)

    def auto_set(self) -> None:
        """
        Trigger MSO autoset
        """
        self.write("AUTOSet EXECute")
        logger.info("AUTOSET executed")

    @property
    def trigger_mode(self) -> str:
        """
        Get trigger mode

        Returns:
            str: trigger mode
        """
        value = self.query("TRIGger:A:MODe?")
        return str(value).strip()

    @trigger_mode.setter
    def trigger_mode(self, trigger_mode: str) -> None:
        """
        Set trigger mode

        Args:   
            trigger_mode: str, ["AUTO", "NORMAL"]

        Returns:
            None
        """
        assert trigger_mode in self.trigger_modes
        self.write(f"TRIGger:A:MODe {trigger_mode}")
        logger.info(f"Trigger mode is set to {self.trigger_mode}")

    @property
    def trigger_type(self) -> str:
        """
        Get trigger type

        Returns:
            str
        """
        value = self.query("TRIGger:A:TYPE?")
        return str(value).strip()

    @trigger_type.setter
    def trigger_type(self, trigger_type: str) -> None:
        """
        Set trigger type

        Args:   
            trigger_type: str, ["EDGE", "LOGIC", "PULSE", "BUS", "VIDEO"]

        Returns:
            None
        """
        assert trigger_type in self.trigger_types
        self.write(f"TRIGger:A:TYPE {trigger_type}")
        logger.info(f"Trigger type is set to {self.trigger_type}")

    @property
    def trigger_slope(self) -> str:
        """
        Get trigger slope

        Returns:
            str
        """
        value = self.query("TRIGger:A:EDGE:SLOpe??")
        return str(value).strip()

    @trigger_slope.setter
    def trigger_slope(self, trigger_slope: str) -> None:
        """
        Set trigger slope

        Args:   
            trigger_slope: str, ["FALL", "RISe"]

        Returns:
            None
        """
        assert trigger_slope in self.trigger_slopes
        self.write(f"TRIGger:A:EDGE:SLOpe {trigger_slope}")
        logger.info(f"Trigger slope is set to {self.trigger_slopes}")

    @property
    def trigger_level(self) -> float:
        """
        Get trigger level

        Returns:
            float: trigger level
        """
        value = self.query("TRIGger:A:LEVEL?")
        return float(value)

    @trigger_level.setter
    def trigger_level(self, trigger_level) -> None:
        """
        set trigger level in user units (usually volts)

        Args: 
            trigger_level: float, trigger level in user units (usually volts)

        Returns:
            None
        """
        self.write(f"TRIGger:A:LEVEL {trigger_level}")
        logger.info(f"Trigger level is set to {self.trigger_level}")

    @property
    def acquire_stop_after(self) -> str:
        """
        Get Acquire stopafter mode

        Returns:
            str: ["RUNST", "SEQ"]
                RUNST: stands for run/stop, MSO will continually acquire data
                SEQ: stands for sequence, only gives a single-sequence acquisition
        """
        value = self.query("ACQuire:STOPAfter?").strip()
        return str(value).replace("\n", "").strip()

    @acquire_stop_after.setter
    def acquire_stop_after(self, stop_after: str) -> None:
        """
        Set ACQuire:STOPAfter

        Args:
            stop_after: ["RUNST", "SEQ"]
                RUNST: stands for run/stop, MSO will continually acquire data
                SEQ: stands for sequence, only gives a single-sequence acquisition
        """
        assert stop_after in self.acquire_stop_afters
        self.write(f"ACQuire:STOPAfter {stop_after}")
        assert stop_after == self.acquire_stop_after
        logger.info(f"ACQuire STOPAfter is set to {stop_after}")

    @property
    def acquire_state(self) -> bool:
        """
        Get acquire state

        Returns:
            bool: run or stop
        """
        value = self.query("ACQuire:STATE?").strip()
        return str2bool(value)

    @acquire_state.setter
    def acquire_state(self, state: bool)->None:
        """
        Set acquire state

        Args: 
            state: bool, run or stop

        Returns:
            None
        """
        assert type(bool(state)) is bool
        self.write(f"ACQuire:STATE {int(state)}")
        assert bool(state) == self.acquire_state
        logger.info(f"ACQuire State is set to {state}")

    def argparser(self, argparser) -> None:
        subparsers = argparser.add_subparsers(
            dest=f"TektronixMSO2024B_{self.device_alias}_command", help='TektronixMSO2024B commands', required=True)
        save_parser = subparsers.add_parser(
            'SAVE', help='save waveform or image', aliases=["save"])
        save_mode_parser = save_parser.add_subparsers(
            dest="SAVE_MODE", help="save waveform or image", required=True)
        save_waveform_parser = save_mode_parser.add_parser(
            'WAVEFORM', help='save waveform', aliases=["waveform"])

        save_waveform_parser.add_argument("--filename",
                                          "--FILENAME",  default="./data/MSO.csv", help="waveform filename to save. .csv ending")
        save_waveform_parser.add_argument("--resolution", "--RESOLUTION", default="REDUCED", choices=[
                                          "FULL", "REDUCED", "full", "reduced"], help="Resolution of waveform. FULL takes a long time")
        save_waveform_parser.add_argument("--gating", "--GATING", default="SCREEN", choices=[
                                          "OFF", "SCREEN", "CURSORS", "off", "screen", "cursors"], help="Resolution of waveform. FULL takes a long time")

        save_image_parser = save_mode_parser.add_parser(
            'IMAGE', help='save image', aliases=["image"])

        save_image_parser.add_argument("--filename",
                                       "--FILENAME",  default="./data/MSO.bmp", help="image filename to save. .bmp ending")

        set_parser = subparsers.add_parser(
            'AUTOSET', help='AUTO set vertical, horizontal, and trigger', aliases=["autoset"])

        set_parser = subparsers.add_parser(
            'SET', help='save waveform or image', aliases=["set"])
        set_parser.add_argument('channel', type=str, choices=[*self.channels, *self.maths, *self.refs, *self.buses, *self.digital_channels],
                                help='channel id, including channels, maths, refs, buses')

        set_mode_parser = set_parser.add_subparsers(
            dest="SET_MODE", help="set channel options", required=True)

        set_label_parser = set_mode_parser.add_parser(
            'LABEL', help='set channel label', aliases=["label"])
        set_label_parser.add_argument("label", help="label name")

        set_position_parser = set_mode_parser.add_parser(
            'POS', help='set channel position in volts', aliases=["pos"])
        set_position_parser.add_argument("position", help="position in volts")

        set_offset_parser = set_mode_parser.add_parser(
            'OFFSET', help='set channel offset in volts', aliases=["offset"])
        set_offset_parser.add_argument("offset", help="offset in volts")

        set_scale_parser = set_mode_parser.add_parser(
            'SCALE', help='set channel position in volts', aliases=["scale"])
        set_scale_parser.add_argument("scale", help="scale value")

        set_gain_parser = set_mode_parser.add_parser(
            'GAIN', help='set channel gain', aliases=["gain"])
        set_gain_parser.add_argument("gain", help="gain value")

        meas_parser = subparsers.add_parser(
            'MEAS', help='save waveform or image', aliases=["meas"])
        meas_parser.add_argument('channel', type=str, choices=[*self.channels, *self.maths],
                                 help='channel id, including channels, maths')

        meas_parser.add_argument(
            "MEAS_MODE", choices=self.measurement_modes, help="measurement mode")

        meas_parser.add_argument('-t', '-T', '--times', '--TIMES', type=int,
                                 default=1, help='times of measurement')
        meas_parser.add_argument('-i', '-I', '--interval', '--INTERVAL', type=float,
                                 default=1, help='time interval between measurements')

        meas_parser.add_argument("--filename",
                                 "--FILENAME",  default="./data/MSO.csv", help="data filename to save. .csv ending for csv, otherwise data will be stored in json format")

        hoir_parser = subparsers.add_parser(
            'HORI', help='horizontal commands', aliases=["hori"])
        hori_mode_parser = hoir_parser.add_subparsers(
            dest="HORI_MODE", help="horizontal command", required=True)
        hori_scale_parser = hori_mode_parser.add_parser(
            'SCALE', help='set horizontal scale', aliases=["scale"])
        hori_scale_parser.add_argument('scale', type=float,
                                       help='horizontal scale in seconds')

        trigger_parser = subparsers.add_parser(
            'TRIG', help='MSO trigger', aliases=["trig"])

        trigger_mode_parser = trigger_parser.add_subparsers(
            dest="TRIG_MODE", help="set trigger options", required=True)
        trigger_mode_mode_parser = trigger_mode_parser.add_parser(
            'MODE', help='set trigger mode', aliases=["mode"])
        trigger_mode_mode_parser.add_argument('mode', type=str, choices=self.trigger_modes,
                                              help='trigger mode, AUTO or NORMAL')
        trigger_mode_type_parser = trigger_mode_parser.add_parser(
            'TYPE', help='set trigger type', aliases=["type"])
        trigger_mode_type_parser.add_argument('type', type=str, choices=self.trigger_types,
                                              help='trigger type')
        trigger_mode_level_parser = trigger_mode_parser.add_parser(
            'LEVEL', help='set trigger level', aliases=["LEVEL"])
        trigger_mode_level_parser.add_argument('level', type=float,
                                               help='trigger level in volts')

        acquire_parser = subparsers.add_parser(
            'ACQ', help='MSO acquire', aliases=["acq"])
        acquire_mode_parser = acquire_parser.add_subparsers(
            dest="ACQ_MODE", help="set acquire options", required=True)
        acquire_mode_state_parser = acquire_mode_parser.add_parser(
            'STATE', help='set acquire state', aliases=["state"])
        acquire_mode_state_parser.add_argument('state', type=str2bool,
                                               help='acquire state, True or False')
        acquire_mode_stop_after_parser = acquire_mode_parser.add_parser(
            'STOP', help='set acqure stop after', aliases=["stop"])
        acquire_mode_stop_after_parser.add_argument('stop_after', type=str, choices=self.acquire_stop_afters,
                                                    help='MSO acquire stop after, RUNST (run/stop, continuously obtaining data) or NORMAL')

        super(TektronixMSO2024B, self).argparser(subparsers)

    def parse_args(self, lab_args) -> None:
        """
        Execute TektronixMSO2024B command based on args

        Returns:
            None
        """
        command = vars(lab_args)[
            f"TektronixMSO2024B_{self.device_alias}_command"].upper()
        if command == "SAVE":
            try:
                mode = vars(lab_args)[f"SAVE_MODE"].upper()
                if mode == "WAVEFORM":
                    self.save_waveform(
                        filename=filename_append_timestamp(lab_args.filename), resolution=lab_args.resolution.upper())
                elif mode == "IMAGE":
                    self.save_img(
                        filename=filename_append_timestamp(lab_args.filename))
            except AssertionError as e:
                traceback.print_exc()
        elif command == "SET":
            set_mode = vars(lab_args)[f"SET_MODE"].upper()
            if set_mode == "LABEL":
                self.set_label(lab_args.channel, lab_args.label)
            elif set_mode == "POS":
                self.set_position(lab_args.channel, lab_args.position)
            elif set_mode == "OFFSET":
                self.set_offset(lab_args.channel, lab_args.offset)
            elif set_mode == "SCALE":
                self.set_scale(lab_args.channel, lab_args.scale)
            elif set_mode == "GAIN":
                self.set_gain(lab_args.channel, lab_args.gain)
        elif command == "HORI":
            HORI_mode = vars(lab_args)[f"HORI_MODE"].upper()
            if HORI_mode == "SCALE":
                self.horizontal_scale = lab_args.scale
        elif command == "MEAS":
            meas_mode = vars(lab_args)[f"MEAS_MODE"].upper()
            self.measure(lab_args.channel, meas_mode,
                         lab_args.times, lab_args.interval, filename=filename_append_timestamp(lab_args.filename))
        elif command == "AUTOSET":
            self.auto_set()
        elif command == "TRIG":
            trig_mode = vars(lab_args)[f"TRIG_MODE"].upper()
            if trig_mode == "MODE":
                self.trigger_mode = lab_args.mode
            elif trig_mode == "TYPE":
                self.trigger_type = lab_args.type
            elif trig_mode == "LEVEL":
                self.trigger_level = lab_args.level
        elif command == "ACQ":
            acq_mode = vars(lab_args)[f"ACQ_MODE"].upper()
            if acq_mode == "STOP":
                self.acquire_stop_after = lab_args.stop_after
            elif acq_mode == "STATE":
                self.acquire_state = lab_args.state

        else:
            super(TektronixMSO2024B, self).parse_args(lab_args, command)


if __name__ == '__main__':
    test = TektronixMSO2024B(SCPIDevice)

