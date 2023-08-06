import ctypes
import numpy as np
from CAM_nncam import CAM
import cv2
import time

# cas slm loading class
class FSLM:
    def __init__(self):
        # check the dll route at your own PC
        self.__dll = ctypes.windll.LoadLibrary(".\sim_files\casmicrostar\SecondDll.dll")
        self.__cols = 1920
        self.__rows = 1080
        self.data_width = 1920
        self.data_height = 1080

    # load generated data by numpy 
    def load(self, img):
        self.__dll.saShowBlock(img, self.data_width, self.data_height, 1920, 0, self.__cols, self.__rows, False)

    # open device: notice that this open API must be used after loading
    def open(self):
            self.__dll.saShowWindow(1)

    # destroy the slm window
    def close(self):
        self.__dll.saCloseWindow()

    # generate slm data pattern
    def get_pattern(self, gray_set = [0, 128],img_height=1080,img_width=1080):
        unit = np.tile(np.uint8(gray_set),int(img_width/len(gray_set)))
        img = np.tile(unit, (img_height,1))
        img = list(img.flatten())
        img_1d = np.ascontiguousarray(img, dtype=int)
        count = int(img_height*img_width)
        # translate into c++ pointer
        c_img_1d = (ctypes.c_double*count)()
        for i in range(0, len(c_img_1d)):
            c_img_1d[i] = img_1d[i]
        return c_img_1d


if __name__ == '__main__':
    slm = FSLM()
    # define grating pattern unit: what the gray unit looks like and how many times it repeats(at pixel scale)
    gray_unit = [0, 85, 170]
    unit_width = 10 
    unit_set = np.repeat(gray_unit,unit_width)

    pattern = slm.get_pattern(unit_set,slm.data_height,slm.data_width)
    slm.load(pattern)
    slm.open()
    time.sleep(1)



    slm.close()
 



