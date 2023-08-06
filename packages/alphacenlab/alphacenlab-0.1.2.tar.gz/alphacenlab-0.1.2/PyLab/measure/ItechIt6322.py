from numpy import FLOATING_POINT_SUPPORT
from .SCPIDevice import SCPIDevice
from .utils import str2bool, save_meas_json_to_file, filename_formatter, filename_append_timestamp
import traceback
import time
import logging

logger = logging.getLogger()


class ItechIt6322(SCPIDevice):
    """
    Deivce Itech It6322 command
    """

    def __init__(self, scpiHandle, device_alias: str = None):
        super(ItechIt6322, self).__init__(scpiHandle)
        self.device_alias = device_alias

    channels = [1, 2, 3]

    @property
    def channel(self)->int:
        """
        Get current channel

        Returns:
            channel id, int
        """
        ret = self.query(f"INSTrument:SELect?")
        return int(ret)

    @channel.setter
    def channel(self, channel)->None:
        """
        Set current channel

        Args:
            channel id, int

        Returns:
            None
        """
        assert channel in self.channels
        self.write(f"INSTrument:SELect CH{channel}")

    @property
    def output(self)->bool:
        ret = self.query(f"OUTPut:STATe?")
        return bool(ret)

    @output.setter
    def output(self, output: bool = False)->None:
        assert type(output) is bool
        self.write(f"OUTPut:STATe {int(output)}")

    def current(self, channel: int, current: float)->None:
        """
        set current
        
        Args:
            channel: channel id
            current: in A

        Returns:
            None
        """
        current = float(current)
        assert type(current) is float

        self.channel = channel
        self.write(f"SOURce:CURRent {current}A")

    def voltage(self, channel: int, voltage):
        """
        set voltage
        
        Args:
            channel: channel id
            voltage: in V

        Returns:
            None
        """
        voltage = float(voltage)
        assert type(voltage) is float
        self.channel = channel
        self.write(f"SOURce:VOLTage {voltage}V")

    def measure_current(self, channel: int)->float:
        """
        Measure current

        Args:
            channel: int
        
        Returns:
            float, current measurement value in A
        """
        assert channel in self.channels
        self.channel = channel
        ret = self.query(f"MEASure:CURRent?")
        return float(ret)

    def measure_voltage(self, channel:int)->float:
        """
        Measure voltage

        Args:
            channel: int
        
        Returns:
            float, voltage measurement value in volts
        """
        assert channel in self.channels
        self.channel = channel
        ret = self.query(f"MEASure:VOLTage?")
        return float(ret)

    # Seems no effect
    # def set_voltage_protection_level(self, channel, max_voltage):
    #     self.channel=channel
    #     ret = self.write(f"VOLTage:PROTection:LEVEl 1V")
    #     pass

    # def get_voltage_protection_state(self, channel: int = 1)->bool:
    #     self.channel=channel
    #     ret = self.query(f"VOLTage:PROTection:STATe?") # query gives <1|0>

    #     return bool(ret)

    # def set_voltage_protection_state(self, channel: int = 1, state: bool = False):
    #     self.channel=channel
    #     pass

    def argparser(self, argparser) -> None:
        """
        ItechIt6322 argparser

        Args:
            argparser: argparser to extend
        
        Returns:
            None
        """
        subparsers = argparser.add_subparsers(
            dest=f"ItechIt6322_{self.device_alias}_command", help='ItechIt6322 commands', required=True)

        set_parser = subparsers.add_parser(
            'SET', help='set voltage or current', aliases=["set"])
        set_parser.add_argument('channel', type=str, choices=[
                                "1", "2", "3"], help='channel to set voltage or current')
        set_parser.add_argument('mode', type=str, choices=[
            "VOLT", "volt", "CURR", "curr"], help='set voltage or current value for specific channel')
        set_parser.add_argument(
            'value', type=float, default="0", help='value for voltage (V) or current (A)')

        meas_parser = subparsers.add_parser(
            'MEAS', help='measurement', aliases=["meas"])
        meas_parser.add_argument('channel', type=str, choices=[
                                 "1", "2", "3"], help='channel id to set voltage or current, choose from {1,2,3}')
        meas_parser.add_argument('mode', type=str, choices=[
            "VOLT", "volt", "CURR", "curr"], help='set voltage or current')
        meas_parser.add_argument('-t', '-T', '--times', '--TIMES', type=int,
                                 default=1, help='times of measurement')
        meas_parser.add_argument('-i', '-I', '--interval', '--INTERVAL', type=float,
                                 default=1, help='time interval between measurements')
        meas_parser.add_argument("--filename",
                                 "--FILENAME",  default="./data/MSO.csv", help="data filename to save. .csv ending for csv, otherwise data will be stored in json format")

        output_parser = subparsers.add_parser(
            'OUTPUT', help='output signal for all channels or not', aliases=["output"])
        output_parser.add_argument('output', type=str2bool, nargs='?',
                                   const=True, default=False, help="Output or not, supports on, off, y, n, 1, 0")
        super(ItechIt6322, self).argparser(subparsers)

    def measure(self, channel, mode, times, interval, filename=None):
        """
        Higher level measurement 

        Args:
            channel: channel id
            mode: measurement mode
            times: number of measurements
            interval: time interval between two measurements
            filename:
        """
        mode = mode.upper()
        assert mode in ["VOLT", "CURR"]
        assert channel in self.channels
        start_time = time.time()
        data = []
        for i in range(times):
            if mode == "VOLT":
                value = self.measure_voltage(int(channel))
            elif mode == "CURR":
                value = self.measure_current(int(channel))
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

        # generate result dict
        result = {
            "metadata": {
                "start_time": start_time,
                "end_time": end_time,
                "device_type": self.__class__.__name__,
                "resource_name": self.inst.resource_name,
                "mode": mode,
                "channel": channel,
            },
            "data": data
        }
        
        # save file if exists
        if filename:
            save_meas_json_to_file(result, filename_formatter(filename))
        return result

    def parse_args(self, lab_args) -> None:
        """
        Execute ItechIt6322 command based on args

        Returns:
            None
        """
        command = vars(lab_args)[
            f"ItechIt6322_{self.device_alias}_command"].upper()
        if command == "SET":
            try:
                mode = lab_args.mode.upper()
                if mode == "VOLT":
                    self.voltage(int(lab_args.channel), float(lab_args.value))
                elif mode == "CURR":
                    self.current(int(lab_args.channel), float(lab_args.value))
            except AssertionError as e:
                traceback.print_exc()

        elif command == "OUTPUT":
            self.output = lab_args.output
        elif command == "MEAS":
            self.measure(lab_args.mode, int(lab_args.channel),
                         lab_args.times, lab_args.interval, filename_append_timestamp(lab_args.filename))
        else:
            super(ItechIt6322, self).parse_args(lab_args, command)
