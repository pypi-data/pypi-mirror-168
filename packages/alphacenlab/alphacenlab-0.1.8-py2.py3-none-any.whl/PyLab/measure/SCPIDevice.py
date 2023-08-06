
from pyvisa import VisaIOError
import json
import logging

logger = logging.getLogger()


class SCPIDevice:

    def __init__(self, scpiHandle):
        self.inst = scpiHandle
        if self.inst is None:
            return
        # default timeout is a little short for resets and other things
        self.inst.timeout = 10000

    def write(self, s, deep=True):
        if deep:
            if self.inst is None:
                [0, 0]
            return self.brvWrite(s)
        else:
            if self.inst is None:
                return
            return self.inst.write(s)

    def read(self):
        if self.inst is None:
            return ""
        try:
            return self.inst.read()
        except:
            return None

    def readTMC(self, blockSize=4096):
        if self.inst is None:
            return ""
        # need to parse the TMC header to find out how many bytes need to be ready
        # this is a candidate for refactoring. this will hardly be the last time i
        # find a TMC header (TMC stands fro Test Measurment and Control)
        # format '#Nxxxxxxxxx'
        # '#' is the start indicator for a TMC header
        # N is the number of bytes in the TMC header left to read
        # xxxx is a decimal number giving the length of the data to follow.
        tmcSizeStr = self.inst.read_bytes(2)
        # todo: throw an exception if the first character is not a '#'
        tmcSize = int(tmcSizeStr[1:])
        byteCount = int(self.inst.read_bytes(tmcSize))
        x = self.inst.read_bytes(byteCount, blockSize)
        return x

    def queryRaw(self, command):
        if self.inst is None:
            return ""
        self.write(command, deep=False)
        return self.inst.read_raw()

    def query(self, s, deep=True):
        if self.inst is None:
            return ""
        if deep:
            return self.brvQuery(s)
        else:
            return self.inst.query(s)

    def queryTMC(self, s):
        if self.inst is None:
            return ""
        try:
            err = self.write(s, deep=False)
            result = self.readTMC(2**16)
        except VisaIOError:
            print("VISAIOERROR")
        x = self.err
        if (x[0] != 0):
            print("ERROR:", x)
        self.write("*CLS", deep=False)
        return result

    def brvWrite(self, val):
        t = ""
        try:
            t = self.write(val, deep=False)
        except VisaIOError:
            print("VISAIOERROR")
        x = self.err
        if (x[0] != 0):
            print("ERROR:", x)
        self.write("*CLS", deep=False)
        return t

    def brvQuery(self, val):
        t = ""
        try:
            t = self.query(val, deep=False)
        except VisaIOError:
            print("VISAIOERROR")
        x = self.err
        if (x[0] != 0):
            print("ERROR:", x)
        self.write("*CLS", deep=False)
        return t

    def reset(self):
        self.write("*RST", deep=False)

    @property
    def err(self):
        tmp = self.query(":SYSTEM:ERROR?", deep=False).strip()
        tmp = tmp.split(',')
        try:
            tmp[0] = int(tmp[0])
        except:
            tmp = [0, 0]
        return tmp

    def argparser(self, argparser) -> None:
        """
        Append SCPI command to parser

        Returns:
            None
        """
        write_parser = argparser.add_parser(
            'WRITE', help='write raw commands to device', aliases=["write"])
        write_parser.add_argument(
            'command', type=str, nargs="+", help='write raw commands, please look at docs for all commands available')
        query_parser = argparser.add_parser(
            'QUERY', help='query raw commands to device', aliases=["query"])
        query_parser.add_argument(
            'command', type=str, nargs="*", help='query raw commands, please look at docs for all commands available')

    def parse_args(self, lab_args, command=None) -> None:
        """
        Execute SCPI command based on args

        Returns:
            None
        """
        if lab_args != None:
            command_to_device = " ".join(lab_args.command)
            if command.upper() == "WRITE":
                ret = self.write(command_to_device)
            elif command.upper() == "QUERY":
                ret = self.query(command_to_device)
            logger.info(
                f"{self.device_alias}: {command} {command_to_device}; return: {ret}")
