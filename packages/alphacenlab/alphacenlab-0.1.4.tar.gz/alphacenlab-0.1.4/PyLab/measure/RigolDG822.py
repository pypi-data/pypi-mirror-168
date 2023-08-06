from .SCPIDevice import SCPIDevice
import argparse
import inquirer
import logging
import traceback
import json
from .utils import str2bool

logger = logging.getLogger()


class RigolDG822(SCPIDevice):
    def __init__(self, scpiHandle, device_alias: str = None):
        super(RigolDG822, self).__init__(scpiHandle)
        self.device_alias = device_alias

    channels = [1, 2]

    sources = {
        "SIN": "SINusoid",
        "DC": "DC",
        "DUALT": "DUALTone",
        "HARM": "HARMonic",
        "NOIS": "NOISe",
        "PRBS": "PRBS",
        "PULS": "PULSe",
        "RAMP": "RAMP",
        "RS232": "RS232",
        "SEQ": "SEQuence",
        "SQU": "SQUare",
        "USER": "User"
    }

    def argparser(self, argparser: argparse.ArgumentParser) -> None:
        """
        Argparse for RigolDG822 commands

        Args:
            argparser: parent argparser

        Returns:
            None
        """

        subparsers = argparser.add_subparsers(
            dest=f"RigolDG822_{self.device_alias}_command", help='RigolDG822 commands', required=True)
        output_parser = subparsers.add_parser(
            'OUTPUT', help='output signal or not', aliases=["output"])
        output_parser.add_argument('channel', type=int, metavar=f"Channel",
                                   choices=self.channels, help='Channel id, choose from {1,2}')
        output_parser.add_argument('output', type=str2bool, nargs='?',
                                   const=True, default=False, help="Output or not, supports on, off, y, n, 1, 0")

        align_parser = subparsers.add_parser(
            'ALIGN', help='Align the signals', aliases=["align"])

        set_waveform_parser = subparsers.add_parser(
            'SET', help='Signal source type, (support all source types)', aliases=["set"])
        set_waveform_parser.add_argument('channel', type=int,
                                         choices=self.channels, help='Channel id, choose from {1,2}')

        waveform_parser = set_waveform_parser.add_subparsers(
            dest="waveform", help='Waveforms to device', required=True)

        sin_parser = waveform_parser.add_parser(
            'SIN', help='Sinusoid wave', aliases=["sin"])
        sin_parser.add_argument('-f', '-F', '--freq', '--FREQ', type=float,
                                default=0, help="frequency in Hz")
        sin_parser.add_argument('-a', '-A', '--amp', '--AMP', type=float,
                                default=0, help="amplitude (Vpp)")
        sin_parser.add_argument('-o', '-O', '--offset', '--OFFSET', type=float,
                                default=0, help="offset (Vdc)")
        sin_parser.add_argument('-p', '-P', '--phase', '--PHASE', type=float,
                                default=0, help="phase in degrees")

        dualtone_parser = waveform_parser.add_parser(
            'DUAL', help='dualtone with 2 frequencies', aliases=["dual"])
        dualtone_parser.add_argument('-f1', '-F1', '--freq1', '--FREQ1', type=float,
                                     default=0, help="frequency 1 in Hz")
        dualtone_parser.add_argument('-f2', '-F2', '--freq2', '--FREQ2', type=float,
                                     default=0, help="frequency 2 in Hz")
        dualtone_parser.add_argument('-a', '-A', '--amp', '--AMP', type=float,
                                     default=0, help="amplitude (Vpp)")
        dualtone_parser.add_argument('-o', '-O', '--offset', '--OFFSET', type=float,
                                     default=0, help="offset (Vdc)")

        square_parser = waveform_parser.add_parser(
            'SQU', help='Sqaure wave with dcycle', aliases=["squ"])
        square_parser.add_argument('-f', '-F', '--freq', '--FREQ', type=float,
                                   default=0, help="frequency in Hz")
        square_parser.add_argument('-a', '-A', '--amp', '--AMP', type=float,
                                   default=0, help="amplitude (Vpp)")
        square_parser.add_argument('-o', '-O', '--offset', '--OFFSET', type=float,
                                   default=0, help="offset (Vdc)")
        square_parser.add_argument('-p', '-P', '--phase', '--PHASE', type=float,
                                   default=0, help="phase in degrees")
        square_parser.add_argument('-d', '-D', '--dcycle', '--DCYCLE', type=float,
                                   default=50, help="square wave dcycle")

        super(RigolDG822, self).argparser(subparsers)

    def parse_args(self, lab_args: argparse.Namespace) -> None:
        """ 
        Parse args for RigolDG822 commands

        Args:
            lab_args: lab arguments from command line

        Returns:
            None
        """
        command = vars(lab_args)[
            f"RigolDG822_{self.device_alias}_command"].upper()
        if command == "SET":
            waveform = lab_args.waveform.upper()
            if waveform == "SIN":
                self.set_source_sin(lab_args.channel, lab_args.freq,
                                    lab_args.amp, lab_args.offset, lab_args.phase)
            elif waveform == "DUAL":
                self.set_source_dualtone(lab_args.channel, lab_args.freq1, lab_args.freq2,
                                         lab_args.amp, lab_args.offset)
            elif waveform == "SQU":
                self.set_source_square(lab_args.channel, lab_args.freq,
                                       lab_args.amp, lab_args.offset, lab_args.phase, lab_args.dcycle)
        elif command == "OUTPUT":
            self.set_output(lab_args.channel, lab_args.output)
        elif command == "ALIGN":
            self.align()
        else:
            return super().parse_args(lab_args, command)

    def inquirer(self) -> None:
        """ 
        Interactive questions for RigolDG822 commands

        Returns:
            None
        """
        def raw_command(command):
            questions = [
                inquirer.Text('command_to_device',
                              message=f"Raw command to the device, please refer to the docs.",
                              ),
            ]
            answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
            command_to_device = answers["command_to_device"]
            if command == "write":
                ret = self.write(command_to_device)
            elif command == "query":
                ret = self.query(command_to_device)
            print(f">>>{self.device_alias} {command} {command_to_device}")
            logger.info(
                f"{self.device_alias}: {command} {command_to_device}; return: {ret}")

        def sin():
            questions = [
                inquirer.List('channel',
                              message="Which channel?",
                              choices=self.channels
                              ),

                inquirer.Text('freq',
                              message=f"frequency in Hz",
                              default="1"
                              ),
                inquirer.Text('amp',
                              message=f"Amplitude in Vpp",
                              default="0"
                              ),
                inquirer.Text('offset',
                              message=f"Offset in Vdc",
                              default="0"
                              ),
                inquirer.Text('phase',
                              message=f"Phase in degrees, from 0 to 360",
                              default="0"
                              ),
            ]
            answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
            self.set_source_sin(**answers)
            print(
                f""">>>{self.device_alias} set {answers["channel"]} SIN -F {answers["freq"]} -A {answers["amp"]} -O {answers["offset"]} -P {answers["phase"]}""")

        def square():
            questions = [
                inquirer.List('channel',
                              message="Which channel?",
                              choices=self.channels
                              ),
                inquirer.Text('freq',
                              message=f"frequency in Hz",
                              default="1"
                              ),
                inquirer.Text('amp',
                              message=f"Amplitude in Vpp",
                              default="0"
                              ),
                inquirer.Text('offset',
                              message=f"Offset in Vdc",
                              default="0"
                              ),
                inquirer.Text('phase',
                              message=f"Phase in degrees, from 0 to 360",
                              default="0"
                              ),
                inquirer.Text('dcycle',
                              message=f"Dcycle in percentage(0-100)",
                              default="50"
                              ),
            ]
            answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
            self.set_source_square(**answers)
            print(
                f""">>>{self.device_alias} set {answers["channel"]} SQU -F {answers["freq"]} -A {answers["amp"]} -O {answers["offset"]} -P {answers["phase"]} -D {answers["dcycle"]}""")

        def dualtone():
            questions = [
                inquirer.List('channel',
                              message="Which channel?",
                              choices=self.channels
                              ),
                inquirer.Text('freq1',
                              message=f"frequency1 in Hz",
                              default="1"
                              ),
                inquirer.Text('freq2',
                              message=f"frequency2 in Hz",
                              default="1"
                              ),
                inquirer.Text('amp',
                              message=f"Amplitude in Vpp",
                              default="0"
                              ),
                inquirer.Text('offset',
                              message=f"Offset in Vdc",
                              default="0"
                              ),
            ]
            answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
            self.set_source_dualtone(**answers)
            print(
                f""">>>{self.device_alias} set {answers["channel"]} SQU -F1 {answers["freq1"]} -F2 {answers["freq2"]} -A {answers["amp"]} -O {answers["offset"]}""")

        def output():
            questions = [
                inquirer.List('channel',
                              message="Which channel?",
                              choices=self.channels
                              ),
                inquirer.List('output',
                              message=f"output or not",
                              choices=[("ON", True), ("OFF", False)]
                              ),

            ]
            answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
            self.set_output(**answers)
            print(
                f""">>>{self.device_alias} output {answers["channel"]} {answers["output"]}""")

        def choose_action():
            questions = [
                inquirer.List('action',
                              message=f"What do you want to do with devicd {self.device_alias}?",
                              choices=[
                                  ("set          set the source signal type", "set"),
                                  ("output          output the signal or not", "output"),
                                  ("align           Align the signals", "align"),
                                  ("write           write raw commands to RigolDM3058E", "write"),
                                  ("query           query raw commands to RigolDM3058E", "query"),
                              ]),
            ]
            answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
            return answers["action"]

        def choose_set_waveform():
            questions = [
                inquirer.List('waveform',
                              message=f"Which waveform u are going to use?",
                              choices=[
                                  "sin",
                                  "dualtone",
                                  "square"
                              ]),
            ]
            answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
            return answers["waveform"]

        # Action based on commands
        action = choose_action()
        if action == "set":
            waveform = choose_set_waveform()
            if waveform == "sin":
                sin()
            elif waveform == "dualtone":
                dualtone()
            elif waveform == "square":
                square()
        elif action == "align":
            self.align()
            print(
                f""">>>{self.device_alias} align""")
        elif action == "output":
            output()
        elif action in ["write", "query"]:
            raw_command(action)

    def source(self, channel: int = 1) -> dict:
        """ 
        Get the channel source state, including waveform, frequency, amplitude, offset and phase

        Args:
            channel: channel id

        Returns:
            waveform: string, self.sources
            freq: float, frequency in Hz, None if not given
            amp: float, amplitude in Vpp, None if not given
            offset: float, offset in Vdc, None if not given
            phase: float, phase shift in degrees, None if not given
        """
        ret = self.query(f":SOURce{channel}:APPLy?")
        results = ret.replace("\n", "").replace("\"", "").split(",")
        waveform = results[0]
        freq = float(results[1]) if results[1] != 'DEF' else None
        amp = float(results[2]) if results[2] != 'DEF' else None
        offset = float(results[3]) if results[3] != 'DEF' else None
        phase = float(
            results[4]) if waveform != "DC" and results[4] != 'DEF' else None
        return {
            "waveform": waveform,
            "freq": freq,
            "amp": amp,
            "offset": offset,
            "phase": phase
        }

    def set_source(self, channel: int = 1, waveform: str = "SIN", freq: float = None, amp: float = None, offset: float = None, phase: float = None):
        """ 
        Set the channel source state, including waveform, frequency, amplitude, offset and phase

        Args:
            channel: channel id
            waveform: string, self.sources
            freq: float, frequency in Hz, None if not given
            amp: float, amplitude in Vpp, None if not given
            offset: float, offset in Vdc, None if not given
            phase: float, phase shift in degrees, None if not given

        Returns:
            None
        """
        assert waveform in self.sources.keys()
        assert channel in self.channels
        amp = 0 if amp is None else float(amp)
        offset = 0 if offset is None else float(offset)
        if waveform in ["RS232"]:
            self.write(
                f":SOURce{channel}:APPLy:{waveform} {amp},{offset}")

        elif waveform in ["DC", "DUALT"]:
            freq = 0 if freq is None else float(freq)
            self.write(
                f":SOURce{channel}:APPLy:{waveform} {freq},{amp},{offset}")

        elif waveform in ["HARM", "SEQ", "SIN", "SQU", "USER"]:
            freq = 0 if freq is None else float(freq)
            phase = 0 if phase is None else float(phase)

            # assert 0 <= phase and phase <= 360

            self.write(
                f":SOURce{channel}:APPLy:{waveform} {freq},{amp},{offset},{phase}")

        # prevent source set failure
        result = self.source(channel)
        try:
            logger.info(
                f"{self.device_alias} channel {channel}: {json.dumps(result, indent=4)}")
            assert result["waveform"] == waveform
            assert result["freq"] == freq
            assert result["amp"] == amp
            assert result["offset"] == offset
            assert result["phase"] == phase
        except AssertionError:
            traceback.print_exc()
            logger.error("Applying waveform failed")

    def output(self, channel: int) -> bool:
        """ 
        Get the channel output state

        Args:
            channel: channel id

        Returns:
            output: bool
        """
        assert channel in self.channels
        ret = self.query(f":OUTPut{channel}?")
        if ret == "ON":
            return True
        elif ret == "OFF":
            return False

    def set_output(self, channel: int, output: bool) -> None:
        """ 
        Set the channel output state

        Args:
            channel: channel id
            output: output state

        Returns:
            None
        """
        assert channel in self.channels
        self.write(f":OUTPut{channel} {int(output)}")
        logger.info(
            f"{self.device_alias} channel {channel}: Output is set to be {output}")

    def align(self, channel: int = 1):
        """
        Align two channels

        Args:
            channel: channel id

        Returns:
            None
        """
        self.write(f":SOURce{channel}:PHASe:SYNChronize")
        logger.info(
            f"{self.device_alias}: sent align command")

    def set_source_DC(self, channel: int = 1, offset: float = 0):
        """
        Set channel to output DC signal

        Args:
            channel: channel id
            offset: float, offset in Vdc, None if not given

        Returns:
            None
        """
        assert channel in self.channels

        # placeholders for command to device
        freq = 0
        amp = 0
        self.write(
            f":SOURce{channel}:APPLy:DC {freq},{amp},{offset}")

        # prevent set waveform failure
        result = self.source(channel)
        try:
            logger.info(
                f"{self.device_alias} channel {channel}: {json.dumps(result, indent=4)}")
            assert result["offset"] == offset
        except AssertionError:
            traceback.print_exc()
            logger.error("Applying waveform failed")

    def set_source_dualtone(self, channel: int = 1, freq1: float = 0, freq2: float = 0, amp: float = 0, offset: float = 0):
        """
        Set channel to output dualtone mode
        F_center = (F_1+F_2)/2
        F_offset = F_2 - F_1

        Args:
            channel: channel id
            freq1: float, frequency 1 in Hz
            freq2: float, frequency 2 in Hz
            amp: float, amplitude in Vpp
            offset: float, offset in Vdc

        Returns:
            None
        """
        assert channel in self.channels
        freq1 = float(freq1)
        freq2 = float(freq2)
        amp = float(amp)
        offset = float(offset)
        self.write(
            f":SOURce{channel}:APPLy:DUALTone {freq1},{amp},{offset}")
        self.write(
            f":SOURce{channel}:FUNCtion:DUALTone:FREQ2 {freq2}")

        # prevent dualtone set failure
        result = self.source(channel)
        result["freq1"] = float(self.query(
            f":SOURce{channel}:FUNCtion:DUALTone:FREQ1?"))
        result["freq2"] = float(self.query(
            f":SOURce{channel}:FUNCtion:DUALTone:FREQ2?"))
        try:
            logger.info(
                f"{self.device_alias} channel {channel}: {json.dumps(result, indent=4)}")
            assert result["freq1"] == freq1
            assert result["freq2"] == freq2
            assert result["amp"] == amp
            assert result["offset"] == offset
        except AssertionError:
            traceback.print_exc()
            logger.error("Applying waveform failed")

    def set_source_sin(self, channel: int = 1, freq: float = 0, amp: float = 0, offset: float = 0, phase: float = 0):
        """
        Set channel to output sinusoid signal

        Args:
            channel: channel id
            waveform: string, self.sources
            freq: float, frequency in Hz
            amp: float, amplitude in Vpp
            offset: float, offset in Vdc
            phase: float, phase shift in degrees

        Returns:
            None
        """
        assert channel in self.channels
        assert 0 <= phase <= 360, "Phase should be in between 0 degrees and 360 degrees"
        freq = float(freq)
        amp = float(amp)
        offset = float(offset)
        phase = float(phase)
        self.write(
            f":SOURce{channel}:APPLy:SINusoid {freq},{amp},{offset},{phase}")
        result = self.source(channel)
        try:
            logger.info(
                f"{self.device_alias} channel {channel}: {json.dumps(result, indent=4)}")
            assert result["freq"] == freq
            assert result["amp"] == amp
            assert result["offset"] == offset
            assert result["phase"] == phase
        except AssertionError:
            traceback.print_exc()
            logger.error("Applying waveform failed")

    def set_source_square(self, rms=True, channel: int = 1, amp: float = 0, offset: float = 0, freq: float = 0, phase: float = 0, dcycle: float = 50):
        """
        Set channel to output sqaure wave

        Args:
            channel: channel id
            waveform: string, self.sources
            freq: float, frequency in Hz
            amp: float, amplitude in Vpp
            offset: float, offset in Vdc
            phase: float, phase shift in degrees
            dcycle: float, duty cycle

        Returns:
            None
        """
        assert channel in self.channels
        assert 0 <= phase <= 360, "Phase should be in between 0 degrees and 360 degrees"
        assert 0 <= dcycle <= 100, "Duty cycle should be in between 0% and 100%"
        freq = float(freq)
        amp = float(amp)
        offset = float(offset)
        phase = float(phase)
        dcycle = float(dcycle)
        if rms:
            self.write(f":SOUR{channel}:VOLT:UNIT VRMS")
        else:
            self.write(f":SOUR{channel}:VOLT:UNIT VPP")
        self.write(
            f":SOURce{channel}:APPLy:SQUare {freq},{amp},{offset},{phase}")
        self.write(f":SOURce{channel}:FUNCtion:SQUare:DCYCle {dcycle}")
        # prevent square set failure
        result = self.source(channel)
        result["dcycle"] = float(self.query(
            f":SOURce{channel}:FUNCtion:SQUare:DCYCle?"))
        try:
            logger.info(
                f"{self.device_alias} channel {channel}: {json.dumps(result, indent=4)}")
            assert result["freq"] == freq
            assert result["amp"] == amp
            assert result["offset"] == offset
            assert result["phase"] == phase
            assert result["dcycle"] == dcycle
        except AssertionError:
            traceback.print_exc()
            logger.error("Applying waveform failed")
