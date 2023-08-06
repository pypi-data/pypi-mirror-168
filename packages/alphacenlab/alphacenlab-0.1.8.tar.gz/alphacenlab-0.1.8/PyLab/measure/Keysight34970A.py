from cgi import test
from hmac import trans_36
import sys
sys.path.append("c:\\Users\\muwei\\Documents\\Lab_Automation\\PyLab")
# print(sys.path)
# from lab import get_scpi_handle
from SCPIDevice import SCPIDevice
from matplotlib import transforms
import pyvisa as visa
import time
import numpy as np
import logging

logger = logging.getLogger()


class DeviceNotFound(Exception):
    """
    Device not found exception
    """
    pass


def get_scpi_handle(usb_address: str) -> visa.resources.Resource:
    """
    Get SCPI handle. SCPI handle is the basis for accessing devices

    Args:
        usb_address: p[artial usb address for matching

    Returns:
        visa.resources.Resource class
    
    Exceptions:
        DeviceNotFound: Cannot connect device with visa
    """
    rm = visa.ResourceManager()
    logger.debug(f"""PyVisa devices: {"; ".join(rm.list_resources())}""")
    for device_address in rm.list_resources():
        if usb_address in device_address:
            scpi_hande = rm.open_resource(device_address)
            return scpi_hande
    raise DeviceNotFound(f"Cannot connect device with visa {usb_address}")


class Keysight34970A(SCPIDevice):
    '''
    Visa address used 'GPIB0::9::INSTR' can be found in Keysight Connection Expert.
     YOU WILL NEED:
     1. Keysight I/O Suite
     2. NI_VISA_488.2 driver for GPIB
     3. turn the 34970A to the GPIB mode
    '''
    def __init__(self, scpiHandle, device_alias: str = None, sch1=101, sch2=103, snum=1, sint=5, sdel=0.1, sp=0):
        super(Keysight34970A, self).__init__(scpiHandle)
        self.device_alias = "GPIB0::9::INSTR"
        self.sch1 = sch1
        self.sch2 = sch2
        self.scan_channel = self.sch2 - self.sch1 + 1
        self.scan_list = "(@{}".format(self.sch1) + ':' + "{})".format(self.sch2)
        self.scan_times = snum
        self.device = None
        self.scan_intervals = sint
        self.scan_delay = sdel
        self.data_points = sp
        self.data_record = list()
        self.data = list()
    
    def connect(self):
        self.device = Keysight34970A(get_scpi_handle(self.device_alias))
        self.device.write("*CLS")
        self.device.write("*RST")

    def scan_config(self,CONF="DC",CH1=101,CH2=103,SCAN=1,INTERVAL=0.1,DELAY=0.1):
        '''
        Config scan measurement, scan time
        '''
        self.sch1 = CH1
        self.sch2 = CH2
        self.scan_times = SCAN
        self.scan_intervals = INTERVAL
        self.scan_delay = DELAY
        measure = {"TEMP":'CONF:TEMP TC,K,', "RES":'CONF:RES ',
                    "DC":'CONF:VOLT:DC ', "AC":'CONF:VOLT:AC ', "FREQ":'CONF:FREQ '}
        logger.info(f"mode {CONF}")
        self.device.write(measure[CONF] + self.scan_list)
        self.device.write("ROUTE:SCAN " + self.scan_list)
        self.device.write("ROUTE:SCAN:SIZE?")
        numberChannels = int(self.device.read())
        print("NumberChannels: ", numberChannels)
        self.device.write("ROUT:CHAN:DELAY " + str(self.scan_delay) + "," + self.scan_list)
        self.device.write("TRIG:COUNT " + str(self.scan_times))
        self.device.write("TRIG:SOUR TIMER")
        self.device.write("TRIG:TIMER " + str(self.scan_intervals))

    def reading_format(self,chan="OFF",time="OFF"):
        '''
        OPTIONAL: reading format configuration
        '''
        self.device.write("FORMAT:READING:CHAN {}".format(chan))
        self.device.write("FORMAT:READING:TIME {}".format(time))
        
    def start_scan(self):    
        self.device.write("INIT;:SYSTEM:TIME:SCAN?")
        print("INIT STATE,", self.device.read())
        # wait until there is a data available
        while (self.data_points == 0):
            self.device.write("DATA:POINTS?")   
            self.data_points=int(self.device.read())
            time.sleep(0.1)
        # scan and data recording
        # for num in range(1, self.scan_times+1): 
        #     self.data_record = list()   
        #     self.device.write("DATA:REMOVE? 1")
        #     self.data_record.append(self.device.read())
        #     for chan in range(1, self.scan_channel+1):
        #         self.device.write("DATA:REMOVE? 1")
        #         self.data_record.append(self.device.read())
        #         self.data_points = 0
        #         while (self.data_points == 0):
        #             self.device.write("DATA:POINTS?")
        #             self.data_points = int(self.device.read())
        time.sleep(self.scan_intervals*(self.scan_times-1))
        success_record = 0
        for num in range(0, self.scan_times*self.scan_channel):
            try:
                self.device.write("DATA:REMOVE? 1")
                self.data_record.append(self.device.read())
                time.sleep(self.scan_delay)
                success_record += 1
            except:
                print("已经记录次数，", success_record+1)
            while (self.data_points == 0):
                self.device.write("DATA:POINTS?")
                self.data_points = int(self.device.read())
        for data in self.data_record:
            record_data = data.strip('\n')
            new_data = float(record_data)
            self.data.append(new_data)
        self.data = np.array(self.data).reshape(self.scan_times,self.scan_channel)
        print("data record: ", self.data)
        self.data = np.mean(self.data,axis=0)
        print("mean data record: ", self.data)

    def close(self):
        self.device.close()
        print("close instrument connection")


if __name__ == '__main__':
    test_34970A = Keysight34970A(SCPIDevice)
    test_34970A.connect()

    test_34970A.scan_config(CONF="RES",CH1=101,CH2=117,SCAN=1,INTERVAL=0.1,DELAY=0.1)
    test_34970A.start_scan()
    raw_data = test_34970A.data_record
    data = test_34970A.data

    test_34970A.close()

