#########################################################################
# FOR PHASE RANGE EXMPERIMENT, YOU WILL NEED:
# signal_fft_phase.py
# phase_fft_main.py
# CAM_ueye.py
# PyLab SDK from EE_Lab_Automation
#########################################################################
from pyueye import ueye
import numpy as np
import cv2
import utils
import time
'''
CCD image caputre for UI3240 ueye
YOU WILL NEED:
1. IDS-UI3240 driver SDK installed
2. IDS-UI3240 python SDK installed
'''

class CAM_ueye():
    def __init__(self,AUTO_EXPO=0,EXPO_TIME=0.01,Bits=8,chan=1,id=0):
        self.hCam = ueye.HIDS(id)                 #0: first available camera;  1-254: The camera with the specified camera ID
        self.sInfo = ueye.SENSORINFO()
        self.cInfo = ueye.CAMINFO()
        self.pcImageMemory = ueye.c_mem_p()
        self.MemID = ueye.int()
        self.rectAOI = ueye.IS_RECT()
        self.pitch = ueye.INT()
        self.nBitsPerPixel = ueye.INT(Bits)     #24: bits per pixel for color mode; take 8 bits per pixel for monochrome
        self.channels = chan                    #3: channels for color mode(RGB); take 1 channel for monochrome
        self.m_nColorMode = ueye.INT()		    # Y8/RGB16/RGB24/REG32
        self.bytes_per_pixel = int( Bits / 8)
        self.auto_expo = AUTO_EXPO
        self.expo_time = EXPO_TIME
        self.nRet = None
        self.m_nColorMode = None
        self.width = self.rectAOI.s32Width
        self.height = self.rectAOI.s32Height

    def open(self):
        self.nRet = ueye.is_InitCamera(self.hCam, None)
        if self.nRet != ueye.IS_SUCCESS:
            print("is_InitCamera ERROR")
        self.nRet = ueye.is_GetCameraInfo(self.hCam, self.cInfo)
        if self.nRet != ueye.IS_SUCCESS:
            print("is_GetCameraInfo ERROR")
        dbleDummy = ueye.c_double(0)    
        # set exposure mode
        if self.auto_expo:
            dbleEnable = ueye.c_double(1)
        else:
            self.nRet = ueye.is_Exposure(self.hCam,ueye.IS_EXPOSURE_CMD_SET_EXPOSURE,
            ueye.c_double(self.expo_time),8)
            dbleEnable = ueye.c_double(0)
        self.nRet = ueye.is_SetAutoParameter(self.hCam, ueye.IS_SET_ENABLE_AUTO_SHUTTER,
        dbleEnable,dbleDummy)
        if self.nRet != ueye.IS_SUCCESS:
            print("AUTO_EXPOSURE ERROR")
        # set display mode to DIB
        self.nRet = ueye.is_SetDisplayMode(self.hCam, ueye.IS_SET_DM_DIB)

        # Set the right color mode
        if int.from_bytes(self.sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_BAYER:
            # setup the color depth to the current windows setting
            ueye.is_GetColorDepth(self.hCam, nBitsPerPixel, m_nColorMode)
            bytes_per_pixel = int(nBitsPerPixel / 8)
            print("IS_COLORMODE_BAYER: ", )
            print("\tm_nColorMode: \t\t", m_nColorMode)
            self.m_nColorMode = m_nColorMode
            print("\tnBitsPerPixel: \t\t", nBitsPerPixel)
            print("\tbytes_per_pixel: \t\t", bytes_per_pixel)
            print()
        elif int.from_bytes(self.sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_CBYCRY:
            # for color camera models use RGB32 mode
            m_nColorMode = ueye.IS_CM_BGRA8_PACKED
            nBitsPerPixel = ueye.INT(32)
            bytes_per_pixel = int(nBitsPerPixel / 8)
            print("IS_COLORMODE_CBYCRY: ", )
            print("\tm_nColorMode: \t\t", m_nColorMode)
            self.m_nColorMode = m_nColorMode
            print("\tnBitsPerPixel: \t\t", nBitsPerPixel)
            print("\tbytes_per_pixel: \t\t", bytes_per_pixel)
            print()
        elif int.from_bytes(self.sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_MONOCHROME:
            # for color camera models use RGB32 mode
            m_nColorMode = ueye.IS_CM_MONO8
            nBitsPerPixel = ueye.INT(8)
            bytes_per_pixel = int(nBitsPerPixel / 8)
            print("IS_COLORMODE_MONOCHROME: ", )
            print("\tm_nColorMode: \t\t", m_nColorMode)
            self.m_nColorMode = m_nColorMode
            print("\tnBitsPerPixel: \t\t", nBitsPerPixel)
            print("\tbytes_per_pixel: \t\t", bytes_per_pixel)
            print()
        else:
            # for monochrome camera models use Y8 mode
            m_nColorMode = ueye.IS_CM_MONO8
            self.m_nColorMode = m_nColorMode
            nBitsPerPixel = ueye.INT(8)
            bytes_per_pixel = int(nBitsPerPixel / 8)
            print("else")
        
        # set the size and position of AOI
        self.nRet = ueye.is_AOI(self.hCam, ueye.IS_AOI_IMAGE_GET_AOI, self.rectAOI, ueye.sizeof(self.rectAOI))
        if self.nRet != ueye.IS_SUCCESS:
            print("is_AOI ERROR")
        # print camera information    
        print("for this camera width,", self.width)                               
        print("for this camera height,", self.height)
        print("Camera model:\t\t", self.sInfo.strSensorName.decode('utf-8'))
        print("Camera serial no.:\t", self.cInfo.SerNo.decode('utf-8'))

    def alloc(self):
        self.nRet = ueye.is_AllocImageMem(self.hCam,self.rectAOI.s32Width,self.rectAOI.s32Height
        ,self.nBitsPerPixel,self.pcImageMemory,self.MemID)
        if self.nRet != ueye.IS_SUCCESS:
            print("is_AllocImageMem ERROR")
        else:
            self.nRet = ueye.is_SetImageMem(self.hCam, self.pcImageMemory, self.MemID)
            if self.nRet != ueye.IS_SUCCESS:
                print("is_SetImageMem ERROR")
            else:
                self.nRet = ueye.is_SetColorMode(self.hCam, self.m_nColorMode)
        self.nRet = ueye.is_CaptureVideo(self.hCam, ueye.IS_DONT_WAIT)
        self.nRet = ueye.is_InquireImageMem(self.hCam, self.pcImageMemory,self.MemID,
            self.width,self.height,self.nBitsPerPixel,self.pitch)
        # self.nRet = ueye.is_CaptureVideo(self.hCam, ueye.IS_DONT_WAIT)
        # if self.nRet == ueye.IS_SUCCESS:
        #     self.nRet = ueye.is_InquireImageMem(self.hCam, self.pcImageMemory,self.MemID,
        #     self.width,self.height,self.nBitsPerPixel,self.pitch)
    
    def read(self,frame_time):
        # count = 1 
        imdata = None
        start_time = time.time()
        while(self.nRet == ueye.IS_SUCCESS):
            imdata = ueye.get_data(self.pcImageMemory, self.width, self.height,self.nBitsPerPixel,
            self.pitch,copy=True)
            delta_time = time.time() - start_time
            if delta_time > frame_time:
                break
            else:
                pass
        imdata = np.reshape(imdata,(self.height.value,self.width.value,self.bytes_per_pixel))
        return imdata

    def close(self):
        self.nRet = ueye.is_FreeImageMem(self.hCam,self.pcImageMemory,self.MemID)
        self.nRet = ueye.is_ExitCamera(self.hCam)
        cv2.destroyAllWindows()
        print("Ueye Camera Closed")


if __name__ == '__main__':
    ccd_test = CAM_ueye(AUTO_EXPO=0,EXPO_TIME=0.01,Bits=8,chan=1,id=0)
    ccd_test.open()
    ccd_test.alloc()

    for i in range(6):
        image = ccd_test.read(0.01667)
        # cv2.imwrite("test_freq1khz_{}V.jpg".format(i+1),image)
        cv2.imshow("test",image)
        cv2.waitKey()
        cv2.destroyAllWindows()

    # image2 = ccd_test.read()
    # cv2.imshow("test",image)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    ccd_test.close()
