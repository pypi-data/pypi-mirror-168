from distutils.command.clean import clean
import signal
from sqlite3 import connect
import threading
import os,sys
import socket
import time
from typing_extensions import Self


def sender_udp(port):
    s_sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_sender.bind(('127.0.0.1', port))
    s_sender.settimeout(1)
    return s_sender

def receiver_udp(port):
    r_receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    r_receiver.bind(('127.0.0.1', port))
    return r_receiver

# Create UDP Socket 
s_control = sender_udp(61540)
s_connect = sender_udp(61541)
s_setparam = sender_udp(61542)
s_getpos = sender_udp(61543)
r_info = receiver_udp(61544)
r_pos = receiver_udp(61545)

# Client Exit
def client_exit():
    print("exit")
    s_control.close()
    s_connect.close()
    s_setparam.close()
    s_getpos.close()
    r_info.close()
    r_pos.close()
    sys.exit(0)  

# Create Exit Event
signal.signal(signal.SIGINT, client_exit)
exit = threading.Event() 

# Define command delay time
def udp_delay(delay_time=0.5):
    time.sleep(delay_time)

# Define info listener, prepared for threading
def info_listener():
    while not exit.is_set():
        receive_data, client_address = r_info.recvfrom(1024)
        print("receiver: ", receive_data,client_address)

# Define position track function
def get_pos():
    s_getpos.sendto(b'10',('127.0.0.1',61558))
    receive_data, client_address = r_pos.recvfrom(1024)
    print("raw_position_data:", receive_data,client_address)
    decode_data = str(receive_data,'utf-8')
    data = eval(decode_data)
    udp_delay(0.02)           # upd_delay, try to match camera speed
    return data




# Create Move Command
class move_udp():
    def __init__(self,SPEED=8,ACC=200,D=60,ABS=30,DAN_F=110,DAN_B=-10):
        self.speed = SPEED                # default turning speed
        self.acc = ACC                    # default acceleration
        self.default_d = D                # default moving distance
        self.cy = 1                       # default distance cycling times
        self.default_abs = ABS            # default absolute distance
        self.pos_count = 0                # count for stable position
        self.stop_count = 0               # count for immediately stop
        self.dan_front = DAN_F            # out of detect area
        self.dan_back = DAN_B             # out of detect area
        self.pos_data = 0                 # default pos data
        self.pos_result = 0               # save calculated angle 
        self.distance = 0.0               # setting moving distance
        self.abs_flag = True              # choose move abs or relative
        self.stop_flag = False            # choose to stop progress immediately
    
    # Connect_udp for each command
    def connect_udp(command):
        def connection(self):
            print("-----SENDING CONNECTION-----")
            try:
                s_connect.sendto(b'1',('127.0.0.1',61558))   # connect
                udp_delay()
            except:
                print("-----CONNECTION FAILED-----")
            return command(self)
        return connection
    
    # position detection for each command
    def pos_detect(self, command_str="RUN_REL_FRONT"):
        try:
            self.pos_count = 0
            self.stop_count = 0
            while self.pos_count < 2:
                pos_data1 = get_pos()
                self.pos_data = pos_data1
                pos_data2 = get_pos()
                self.pos_data = pos_data2
                if abs(pos_data2 - pos_data1) < 0.005:
                    self.pos_count += 1
                if self.pos_data > self.dan_front or self.pos_data < self.dan_back:
                    self.stop_count += 1    
                if self.stop_count > 3:
                    self.stop_flag = True
                    self.stop()
            udp_delay()
            print("-----SUCCESSFULLY {}-----".format(command_str))
        except:
            print("-----POS DETECTION FAIL-----")

    # move command
    @connect_udp
    def return_zero(self):
        s_control.sendto(b'3',('127.0.0.1',61558))
        udp_delay()
        self.pos_detect("RETURNED")
    
    @connect_udp
    def stop(self):
        s_control.sendto(b'4',('127.0.0.1',61558))
        udp_delay()
        self.stop_flag = True
        print("-----RUNNING STOPPED------")
        client_exit()

    @connect_udp
    def run_rel_front(self):
        s_control.sendto(b'5',('127.0.0.1',61558))
        udp_delay()
        self.pos_detect("RUN_REL_FRONT")
    
    @connect_udp
    def run_rel_back(self):
        s_control.sendto(b'6',('127.0.0.1',61558))
        udp_delay()
        self.pos_detect("RUN_REL_BACK")

    @connect_udp
    def run_abs(self):
        s_control.sendto(b'7',('127.0.0.1',61558))
        udp_delay()
        self.pos_detect("RUN_ABSOLUTE")
        
    @connect_udp
    def run_cy_front(self):
        s_control.sendto(b'8',('127.0.0.1',61558))
        udp_delay()
        self.pos_detect("RUN_CY_FRONT")

    @connect_udp
    def run_cy_back(self):
        s_control.sendto(b'9',('127.0.0.1',61558))
        udp_delay()
        self.pos_detect("RUN_CY_BACK")

    # Set default parameters
    @connect_udp
    def set_param(self):
        param1 = (hex(self.speed).replace('0x', '')).zfill(4)
        param2 = (hex(self.acc).replace('0x', '')).zfill(4)
        param3 = (hex(self.default_d).replace('0x', '')).zfill(4)
        param4 = (hex(self.cy).replace('0x', '')).zfill(4)
        param5 = (hex(self.default_abs).replace('0x', '')).zfill(4)
        param = str(param1)+str(param2)+str(param3)+str(param4)+str(param5)
        try:
            s_setparam.sendto(b'2',('127.0.0.1',61558))
            udp_delay(0.1)
            s_setparam.sendto(param.encode(),('127.0.0.1',61559))
            udp_delay(1)
        except:
            print('-----COMMAND FAIL: SET PARAM-----')
    
    # Set move parameters
    @connect_udp
    def set_move(self):
        d_string = str(self.distance)
        if self.abs_flag:
            try:
                s_setparam.sendto(b'12',('127.0.0.1',61558))
                udp_delay(0.1)
                s_setparam.sendto(d_string.encode(),('127.0.0.1',61559))
                udp_delay()
            except:
                print('-----COMMAND FAIL: MOVE ABS-----')
        else:
            try:
                s_setparam.sendto(b'11',('127.0.0.1',61558))
                udp_delay(0.1)
                s_setparam.sendto(d_string.encode(),('127.0.0.1',61559))
                udp_delay()
            except:
                print('-----COMMAND FAIL: MOVE RELATIVE-----')

    def absolute(self, distance):
        self.abs_flag = True
        self.distance = distance
        self.set_move()
        self.run_abs()
    
    def relative(self, distance,front=True):
        self.abs_flag = False
        self.distance = distance
        self.set_move()
        if front:
            self.run_rel_front()
        else:
            self.run_rel_back()




    
if __name__ == "__main__":
    test = move_udp()
    Listener =  threading.Thread(None, info_listener)
    Listener.start()
    
    test.return_zero()
    test.speed, test.acc, test.default_d, test.default_abs, test.cy = 8, 200, 60, 30, 1
    test.dan_front = 50
    test.set_param()
    # test.distance = 100.0
    # test.abs_flag = True
    # test.set_move()
    # # test.run_rel_front()
    # # test.return_zero()
    # test.run_abs()
    # test.distance = 6.66
    # test.abs_flag = False
    # test.set_move()
    # # test.return_zero()
    # # test.run_cy_front()     # 按distance进行循环
    # test.run_rel_front()
    # # test.run_rel_back()

    test.absolute(60)
    test.relative(0.1,front=True)
    test.relative(0.1,front=True)
    test.relative(0.1,front=True)    
    test.relative(10,front=False)

    exit.is_set


