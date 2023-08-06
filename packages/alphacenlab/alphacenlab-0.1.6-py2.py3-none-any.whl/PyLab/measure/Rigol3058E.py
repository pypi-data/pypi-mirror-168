import logging
import pyvisa as visa
from pyvisa import VisaIOError
import time
import engineering_notation
from enum import Enum
from .SCPIDevice import SCPIDevice
import inquirer
import traceback
from .utils import save_meas_json_to_file, filename_formatter

logger = logging.getLogger()


class Rigol3058E(SCPIDevice):
    # consts
    dmmModes = {
        'DCV': 'VOLTage:DC',
        'ACV': 'VOLTage:AC',
        'DCI': 'CURRent:DC',
        'ACI': 'CURRent:AC',
        '2WR': 'RESistance',
        'CAP': 'CAPacitance',
        'CONT': 'CONTinuity',
        '4WR': 'FRESistance',
        'DIODE': 'Diode',
        'FREQ': 'FREQuency',
        'PERI': 'PERiod'
    }

    def __init__(self, scpiHandle, device_alias: str = None):
        engineering_notation.engineering_notation._exponent_lookup_scaled['-9'] = "E"
        super(Rigol3058E, self).__init__(scpiHandle)
        self.device_alias = device_alias
        try:
            self.func = "DCV"
        except VisaIOError:
            print("cant set function")

    @property
    def func(self):
        return str(self.query(":FUNC?")).strip()

    @func.setter
    def func(self, val):
        assert val in Rigol3058E.dmmModes.keys()

        tmp = self.write(':FUNCtion:{0}'.format(Rigol3058E.dmmModes[val]))
        self.internalFunction = val
        return tmp

    @property
    def funcs(self)->dict:
        """
        Get All funcs
        
        Returns:
            dict: {
                "key": "func",
                "value": [
                    {
                    "key": "DCV",
                    "description": "DC Voltage",
                    },
                    ...
                ]
            }
        """

        return {
            "key": "func",
            "value": [
                {
                    "key": "DCV",
                    "description": "DC Voltage",
                },
                {
                    "key": "ACV",
                    "description": "AC Voltage",
                },
                {
                    "key": "DCI",
                    "description": "DC CURRent",
                },
                {
                    "key": "ACI",
                    "description": "AC CURRent",
                },
                {
                    "key": "2WR",
                    "description": "RESistance",
                },
                {
                    "key": "CAP",
                    "description": "CAPacitance",
                },
                {
                    "key": "CONT",
                    "description": "CONTinuity",
                },
                {
                    "key": "4WR",
                    "description": "FRESistance",
                },
                {
                    "key": "DIODE",
                    "description": "Diode",
                },
                {
                    "key": "FREQ",
                    "description": "FREQuency",
                },
                {
                    "key": "PERI",
                    "description": "PERiod",
                },
            ],
            "description": "measuring mode",
        }

    @property
    def ranges(self)->list:
        """
        Get All ranges for current func
        
        Returns:
            dict: [
                {
                    "key": "0",
                    "description": "200 mV; resolution 100 nV",
                },
                ...
            ]
        """
        # remove \n returned from device
        _func = self.func.replace("\n", "")

        def range_property():
            if _func == "DCV":
                return [
                    {
                        "key": "0",
                        "description": "200 mV; resolution 100 nV",
                    },
                    {
                        "key": "1",
                        "description": "2 V; resolution 1 μV",
                    },
                    {
                        "key": "2",
                        "description": "20 V; resolution 10 μV",
                    },
                    {
                        "key": "3",
                        "description": "200 V; resolution 100 μV",
                    },
                    {
                        "key": "4",
                        "description": "1000 V; resolution 1 mV",
                    },
                    {
                        "key": "MIN",
                        "description": "Minimum: 200 mV; resolution 100 nV",
                    },
                    {
                        "key": "MAX",
                        "description": "Maximum: 1000 V; resolution 1 mV",
                    },
                    {
                        "key": "DEF",
                        "description": "Default: 20 V; resolution 10 μV",
                    },
                ]
            elif _func == "ACV" or _func == "FREQ" or _func == "PERI":
                return [{
                    "key": "0",
                    "description": "200 mV",
                },
                    {
                        "key": "1",
                        "description": "2 V",
                },
                    {
                        "key": "2",
                        "description": "20 V",
                },
                    {
                        "key": "3",
                        "description": "200 V",
                },
                    {
                        "key": "4",
                        "description": "750 V",
                },
                    {
                        "key": "MIN",
                        "description": "Minimum: 200 mV",
                },
                    {
                        "key": "MAX",
                        "description": "Maximum: 750 V",
                },
                    {
                        "key": "DEF",
                        "description": "Default: 20 V",
                }, ]
            elif _func == "DCI":
                return[{
                    "key": "0",
                    "description": "200 μA; resolution 1 nA",
                },
                    {
                    "key": "1",
                    "description": "2 mA; resolution 10 nA",
                },
                    {
                    "key": "2",
                    "description": "20 mA; resolution 100 nA",
                },
                    {
                    "key": "3",
                    "description": "200 mA; resolution 1 μA",
                },
                    {
                    "key": "4",
                    "description": "2 A; resolution 10 μA",
                },
                    {
                    "key": "5",
                    "description": "10 A; resolution 100 μA",
                },
                    {
                    "key": "MIN",
                    "description": "Minimum: 200 μA; resolution 1 nA",
                },
                    {
                    "key": "MAX",
                    "description": "Maximum: 10 A; resolution 100 μA",
                },
                    {
                    "key": "DEF",
                    "description": "Default: 200 mA; resolution 1 μA",
                },
                ]
            elif _func == "ACI":
                return [{
                    "key": "0",
                    "description": "20 mA",
                }, {
                    "key": "1",
                    "description": "200 mA",
                },
                    {
                        "key": "2",
                        "description": "2 A",
                },
                    {
                        "key": "3",
                        "description": "10 A",
                },
                    {
                        "key": "MIN",
                        "description": "Minimum: 20 mA",
                },
                    {
                        "key": "MAX",
                        "description": "Maximum: 10 A",
                },
                    {
                        "key": "DEF",
                        "description": "Default: 200 mA",
                }, ]
            elif _func == "2WR" or _func == "4WR":
                return [{
                    "key": "0",
                    "description": "200 Ω",
                }, {
                    "key": "1",
                    "description": "2 kΩ",
                },
                    {
                        "key": "2",
                        "description": "20 kΩ",
                },
                    {
                        "key": "3",
                        "description": "200 kΩ",
                },
                    {
                        "key": "4",
                        "description": "1 MΩ",
                },
                    {
                        "key": "5",
                        "description": "10 MΩ",
                },
                    {
                        "key": "6",
                        "description": "100 MΩ",
                },
                    {
                        "key": "MIN",
                        "description": "Minimum: 200 Ω",
                },
                    {
                        "key": "MAX",
                        "description": "Maximum: 100 MΩ",
                },
                    {
                        "key": "DEF",
                        "description": "Default: 200 kΩ",
                }, ]
            elif _func == "CONT":
                return [{
                    "key": "10",
                        "description": "10 Ω for default; This is a consecutive integer ranging form 1 Ω to 2000 Ω.",
                        }]
            elif _func == "CAP":
                return [{
                    "key": "0",
                    "description": "2 nF",
                }, {
                    "key": "1",
                    "description": "20 nF",
                },
                    {
                        "key": "2",
                        "description": "200 nF",
                },
                    {
                        "key": "3",
                        "description": "2 μF",
                },
                    {
                        "key": "4",
                        "description": "200 μF",
                },
                    {
                        "key": "5",
                        "description": "10000 μF",
                },
                    {
                        "key": "MIN",
                        "description": "Minimum: 2 nF",
                },
                    {
                        "key": "MAX",
                        "description": "Maximum: 200 nF",
                },
                    {
                        "key": "DEF",
                        "description": "Default: 10000 μF",
                }, ]

        return {
            "key": "range",
            "value": range_property(),
            "description": "range of measuring mode",
        }

    def func_inquirer(self) -> None:
        """
        Set the measuring mode and range in interactive mode.

        Returns:
            None
        """
        def get_func(funcs):
            questions = [
                inquirer.List('func',
                              message="Which measuring mode?",
                              choices=[(value["description"], value["key"])
                                       for value in funcs]
                              ),
            ]
            answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
            return answers["func"]

        def get_range(ranges):
            questions = [
                inquirer.List('range',
                              message="Which range?",
                              choices=[(value["description"], value["key"])
                                       for value in ranges]
                              ),
            ]
            answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
            return answers["range"]
        func = get_func(self.funcs["value"])
        range = get_range(self.ranges["value"])
        self.func = func
        self.range = range
        print(f">>>{self.device_alias} set {func} {range}")

    def argparser(self, argparser) -> None:
        """
        Append Rigol3058E command to parser

        Returns:
            None
        """
        subparsers = argparser.add_subparsers(
            dest=f"Rigol3058E_{self.device_alias}_command", help='Rigol3058E commands', required=True)

        set_parser = subparsers.add_parser(
            'SET', help='set measuring mode and range',aliases=["set"])
        set_parser.add_argument('mode', type=str, choices=[
                                item["key"] for item in self.funcs["value"]], help='measuring mode')
        set_parser.add_argument(
            'range', type=str, default="DEF", help='measuring range')

        meas_parser = subparsers.add_parser('MEAS', help='measurement',aliases=["meas"])
        meas_parser.add_argument('-t', '-T', '--times', '--TIMES', type=int,
                                 default=1, help='times of measurement')
        meas_parser.add_argument('-i', '-I', '--interval', '--INTERVAL', type=float,
                                 default=1, help='time interval between measurements')

        meas_parser.add_argument("--filename",
         "--FILENAME",  default="./data/DMM.csv", help="data filename to save. .csv ending for csv, otherwise data will be stored in json format")

        super(Rigol3058E, self).argparser(subparsers)

    def parse_args(self, lab_args) -> None:
        """
        Execute Rigol3058E command based on args

        Returns:
            None
        """
        command = vars(lab_args)[f"Rigol3058E_{self.device_alias}_command"]
        if command == "set":
            try:
                self.func = lab_args.mode
                self.range = lab_args.range
            except AssertionError as e:
                traceback.print_exc()

        elif command == "meas":
            self.measure(lab_args.times, lab_args.interval)
        else:
            super(Rigol3058E, self).parse_args(lab_args, command)

    def inquirer(self):
        """
        Rigol3058E interactive inquirer

        Returns:
            None
        """
        def meas():
            questions = [
                inquirer.Text(
                    name='times', message="Times of measurements, default 1", default=1),
                inquirer.Text(name='interval',
                              message="Time interval between measurements, default 1s", default=1),
            ]
            answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
            print(
                f""">>> {self.device_alias} meas --times {answers["times"]} --interval {answers["interval"]}""")
            result = self.measure(int(
                answers["times"]), float(answers["interval"]))
            print(result)
            return int(answers["times"]), float(answers["interval"])

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

        def choose_action():
            questions = [
                inquirer.List('action',
                              message=f"What do you want to do with devicd {self.device_alias}?",
                              choices=[
                                  ("set mode range  set measuring mode and corresponding range", "set"),
                                  ("meas            measurement", "meas"),
                                  ("write           write raw commands to RigolDM3058E", "write"),
                                  ("query           query raw commands to RigolDM3058E", "query"),
                              ]),
            ]
            answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
            return answers["action"]

        # Action based on commands
        action = choose_action()
        if action == "set":
            self.func_inquirer()
        elif action == "meas":
            meas()
        elif action in ["write", "query", ]:
            raw_command(action)

    def measure(self, times, interval,filename = None):
        """
        Measure result. Higher level API.
        
        """
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
                "func": self.func,
                "mode": self.func,
            },
            "data": data
        }
        if filename:
            save_meas_json_to_file(result,filename_formatter(filename))
        return result

    def reset(self):
        super(Rigol3058E, self).reset()
        self.write('CMDSET RIGOL')
        time.sleep(2)
        self.func = "DCV"
        time.sleep(1)
        # default to 200mV scale
        self.write(':MEAS:VOLT:DC 0')

    @property
    def rate(self):
        tmp = self.query(
            ":RATE:{0}?".format(Rigol3058E.dmmModes[self.internalFunction]), deep=False)
        return tmp

    @rate.setter
    def rate(self, val):
        self.write(":RATE:{0} {1}".format(
            Rigol3058E.dmmModes[self.internalFunction], val), deep=False)

    @property
    def range(self):
        tmp = self.query(
            ":MEAS:{0}:RANGE?".format(Rigol3058E.dmmModes[self.internalFunction]), deep=False)
        return tmp

    @range.setter
    def range(self, val):
        assert val in [item["key"] for item in self.ranges["value"]]
        self.write(
            ":MEAS:{0} {1}".format(Rigol3058E.dmmModes[self.internalFunction], val), deep=False)

    def get_val(self):
        tmp = self.query(":MEASure:{0}?".format(
            Rigol3058E.dmmModes[self.internalFunction]), deep=False)
        return float(tmp)

    def calibrate(self, step):
        try:
            if ("step" in step):
                tmp = self.query(':CALI:{0}'.format(step), deep=False)
            else:
                tmp = self.write(':CALI:{0}'.format(step))
            print(tmp)
        except VisaIOError:
            print("im sorry dave, im afraid i cant do that")
            return

        while (int(self.query(":CALI:STATUS?", deep=False))):
            print('.', end='')
            time.sleep(.5)
