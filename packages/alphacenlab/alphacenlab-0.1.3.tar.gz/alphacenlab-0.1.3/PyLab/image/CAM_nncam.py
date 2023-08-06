# cam handler for nncam

# from socketserver import ThreadingUnixStreamServer
# from telnetlib import NOP
from asyncore import read
from distutils.log import ERROR
from logging import error
import threading
import cv2
from cv2 import waitKey
import sys
# you should check this path match your lab automation path
sys.path.insert(0, r'C:\\Users\\muwei\\Documents\\Lab_Automation\\PyLab\\image')
from cam_files import nncam
from threading import Event
from PIL import Image
import numpy as np
import func_timeout
import time

class CAM():
    def __init__(self, MONO=True, AUTO_EXPO=0, EXPO_TIME=11, GAIN=100, CONTRAST=0,VF=True,HF=False):
        self.hcam = None
        self.buf = None
        self.total = 0
        self.snap_flag = None
        # TODO
        self.mono = MONO               # set the color mode to color or gray
        self.auto_expo = AUTO_EXPO     # default 0:mute auto exposure, 1:auto exposure,2:auto exposure single mode 
        self.expo_time = EXPO_TIME     # default exposure time 0.011ms
        self.gain = GAIN               # default image gain 100
        self.contrast = CONTRAST       # default contrast 0
        self.VFlip = VF                # default Vertical flip TRUE
        self.HFlip = HF                # default Horizontal flip FALSE
        self.image_count = 0           # image counter for each time getting new image from buffer
        self.event = threading.Event() # snap only after buffer gets a new image
        # pass the variables to self
        # eg exposure, auto WB, auto exposure, gain, etc. 

    # camera image event callback
    @staticmethod
    def cameraCallback(nEvent, ctx):
        if nEvent == nncam.NNCAM_EVENT_IMAGE:
            ctx.CameraCallback(nEvent)

    def CameraCallback(self, nEvent):
        if nEvent == nncam.NNCAM_EVENT_IMAGE:
            try:
                self.hcam.PullImageV3(self.buf, 0, 24, 0, None)
                self.total += 1
                # TODO       
                self.event.set()
                self.image_count += 1
                # set flag to mark the new image get from buffer
                # print('pull image ok, total = {}'.format(self.total))
            except nncam.HRESULTException as ex:
                print('pull image failed, hr=0x{:x}'.format(ex.hr & 0xffffffff))
        else:
            print('event callback: {}'.format(nEvent))
        
    # open the camera and start the camera callback
    def open(self):
        a = nncam.Nncam.EnumV2()
        if len(a) > 0:
            print('{}: flag = {:#x}, preview = {}, still = {}'.format(a[0].displayname, a[0].model.flag, a[0].model.preview, a[0].model.still))
            # TODO
            # optional & challenge
            # check if use USB 2.0 port 
            # exit and report error for this case
            for r in a[0].model.res:
                print('\t = [{} x {}]'.format(r.width, r.height))
            self.hcam = nncam.Nncam.Open(a[0].id)
            # TODO
            self.hcam.put_Contrast(self.contrast)
            self.hcam.put_AutoExpoEnable(self.auto_expo)
            self.hcam.put_ExpoTime(self.expo_time)
            self.hcam.put_ExpoAGain(self.gain)
            self.hcam.put_VFlip(self.VFlip)
            self.hcam.put_HFlip(self.HFlip)
            self.hcam.put_Chrome(self.mono)
            # set the settings(exposure,gain,flip,etc) 
            # HERE
            if self.hcam:
                width, height = self.hcam.get_Size()
                bufsize = nncam.TDIBWIDTHBYTES(width * 24) * height
                print('image size: {} x {}, bufsize = {}'.format(width, height, bufsize))
                self.buf = bytes(bufsize)
                if self.buf:
                    try:
                        self.hcam.StartPullModeWithCallback(self.cameraCallback, self)
                    except nncam.HRESULTException as ex:
                        print('failed to start camera, hr=0x{:x}'.format(ex.hr & 0xffffffff))
            else:
                print('failed to open camera')
        else:
            print('no camera found')

    # set the timeout callback        
    @func_timeout.func_set_timeout(1)
    def trigger_event(self):
        while not self.event.isSet():
            print("......Image Buffer Wait for loading......")
            self.event.wait()
    
    # when call return a rgb image
    def read(self):
        width, height = self.hcam.get_Size()
        # TODO
        try:  
            self.trigger_event()
        except func_timeout.exceptions.FunctionTimedOut:
            error("__WAITING TIMEOUT__")
            exit()
        # Check the update flag HERE
        # wait until the update flag is true
        image = Image.frombuffer('RGB',(width,height),self.buf,"raw",'RGB',0,1)
        image = np.array(image)
        # TODO 
        # tune the image to the right color sequence R G B
        # tune the image to the right rotation flip/angle
        # OUTPUT IMAGE SHOULD BE COLOR IMAGE and consistent with the sdk preview
        self.image_flag = False
        self.event.clear()
        return image
    
    # close the camera
    def close(self):
        self.hcam.Close()
        self.hcam = None
        self.buf = None
    



if __name__ == '__main__':
    # init
    ccd_test = CAM(MONO=True, AUTO_EXPO=0, EXPO_TIME=25, GAIN=100, CONTRAST=0,VF=True,HF=False)
    # open cam
    ccd_test.open()
    # wait for the fully opening
    time.sleep(0.1)

    # # read images
    # for i in range(1000):
    #     image = ccd_test.read()  # resize the image for better demonstration
    #     image = cv2.resize(image, (0,0), fx=0.5, fy=0.5)
    #     cv2.imshow("test",image)
    #     cv2.waitKey(1)

    image = ccd_test.read()  # resize the image for better demonstration
    cv2.imshow("test",image)
    cv2.imwrite("rawimg.bmp",image)

    cv2.destroyAllWindows

    ccd_test.close()
