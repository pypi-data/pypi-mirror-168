import numpy as np
from slm_files.holoeye import slmdisplaysdk
from slm_files.showSLMPreview import showSLMPreview
import numpy as np
from CAM_nncam import CAM
import cv2
import time

class SLM:
    def __init__(self):
        self.slm = slmdisplaysdk.SLMInstance()
        self.dataWidth = 1024
        self.dataHeight = 768

    # open slm, set PREVIEW to true to open the preview window
    def open(self, PREVIEW = True):
        if not self.slm.requiresVersion(3):
            exit(1)
        # Detect SLMs and open a window on the selected SLM
        error = self.slm.open()
        assert error == slmdisplaysdk.ErrorCode.NoError, self.slm.errorString(error)
        if PREVIEW:
            # Open the SLM preview window in "Fit" mode:
            showSLMPreview(self.slm, scale=0.0) 

    # load pattern to SLM, encode range:256 divided by 2^6 for 16 channel or 4 channel
    def load(self, img):
        # TODO
        # check if necessary for each load?
        data = slmdisplaysdk.createFieldUChar(self.dataWidth, self.dataHeight)
        data = img
        # Show data on SLM: 
        error = self.slm.showData(data)
        assert error == slmdisplaysdk.ErrorCode.NoError, self.slm.errorString(error)

    # destroy the slm class
    def close(self):
        self.slm = None

# generate the vertical stripes
def get_vstripe_pattern(voltage_set = [50,100,150,200],img_height = 768,img_width=1024):
    unit = np.tile(np.uint8(voltage_set),int(img_width/len(voltage_set))) 
    img= np.tile(unit, (img_height,1))         # or phase np.uint8((k+1)*(255/16)) to voltage: vol[k]
    return img


# havent fully tested yet
if __name__ == '__main__':
    cam = CAM()
    cam.expo_time = 20
    slm_test = SLM()
    
    cam.open()
    slm_test.open(PREVIEW=True)

    
    img = get_vstripe_pattern([0,140,168,255],slm_test.dataHeight,slm_test.dataWidth)
    slm_test.load(img)
    time.sleep(0.25)

    cv2.imshow('slm',img)

    cv2.imwrite('SLM_pattern.bmp',img)

    
    img = cam.read()
    cv2.imwrite('SLM_capture.bmp',img)
    img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
    # displaying the image
    cv2.imshow('image', img)
    cv2.waitKey(0)


    





    cam.close()
    slm_test.close()
