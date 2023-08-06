from statistics import mean
from turtle import end_fill
import numpy as np
np.seterr(divide="ignore", invalid='ignore')                                # numpy maybe occur 0 divide 0
import cv2
import csv
import os
from matplotlib import pyplot as plt
import math


def load_data(route='diff_plot1.png', scale=0, index=0, rot_angle=0,start=250,end=800):       # scale 3and index 1define the scanning area
    im_data = cv2.imread(route, cv2.IMREAD_GRAYSCALE)                # (0，0) the data will be at the center bright area
    # Image Rotate
    (h, w) = im_data.shape[:2]                           # [:2] sort line 0 and 1 [;,2] sort the third row for all lines
    (x, y) = (w//2, h//2)
    rotate = cv2.getRotationMatrix2D((x, y), rot_angle, 1.0)                                     # angle -> rotate angle
    cos = np.abs(rotate[0, 0])
    sin = np.abs(rotate[0, 1])
    nw = int((h*sin)+(w*cos))
    nh = int((h*cos)+(w*sin))
    rotate[0, 2] += (nw/2) - x
    rotate[1, 2] += (nh/2) - y
    im_rotate = cv2.warpAffine(im_data, rotate, (nw, nh))

    # blur process，gaussian matrix (5,5)
    im_blur = cv2.blur(im_rotate, (5, 5))

    # contrast increasing, clipLimit 1
    clahe = cv2.createCLAHE(1, (8, 8))                  # clipLimit, threshold number of contrast
    im_clahe = clahe.apply(im_blur)

    # image cutting
    for i in range(h):
        if i < int(h//4) or i > int(3*h//4):
            im_clahe[i, ...] = 10

    # cv2.imshow('test2', im_clahe)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    pixel_data = np.array(im_clahe)
    # print(pixel_data)
    im_len = pixel_data.shape                          # image data resolution
    sum_data_h = [0] * im_len[0]
    sum_data_w = [0] * im_len[1]
    for i in range(2, im_len[0] - 10):                  # intensity sum from 2 to len-2 to avoid margin
        sum_data_h[i] = sum(pixel_data[i])
        sum_data_w[i] = sum(pixel_data[:, i])
        roi_h = sum_data_h.index(max(sum_data_h))
        roi_w = sum_data_w.index(max(sum_data_w))
    # print(roi_w)
    # print(im_len)
    data_len_h = roi_h - index + scale
    data_len_w = roi_w - index + scale
    data_set = np.zeros((scale, im_clahe.shape[1]))
    # get_mean_data for 10 pixel lines
    for i in range(scale):
        data_set[i] = pixel_data[data_len_h - index + i, ...]
    data_set_h = np.zeros((scale, im_clahe.shape[1]))
    # get_mean_data for 10 pixel lines
    for i in range(scale):
        data_set_h[i] = pixel_data[data_len_h - index + i, ...]
    # print(data_set_h)
    data = np.mean(data_set_h, axis=0)  # data at h side
    data = data / 255
    cropped_data = data[start:end]
    # check the line
    for k in range(5):
        im_clahe[data_len_h - 2 + k, ...] = 255
        im_clahe[..., data_len_w + k] = 255
    im_clahe = cv2.rectangle(im_clahe,(300,100),(580,800),(100,255,50),4)
    cv2.imshow('testWinFinal', im_clahe)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    coordinate = [roi_h, roi_w]
    return cropped_data, roi_h

def mean_data(start=250,end=800,id=9,repeat=3):
    dict = {1:0.5,2:1,3:1.5,4:2,5:2.5,6:3,7:3.5,8:4,9:4.5,10:5,11:5.5,12:6,13:6.5,14:7,15:7.5,16:8,17:8.5,18:9,19:9.5,20:10}
    total_data = np.zeros((repeat,end-start))
    for i in range(repeat):
        route = 'phaseac0729/{}v-'.format(dict[id+1]) + '3.jpg' #.format(i+1)
        total_data[i,...] = load_data(route,20,10,0,start,end)
    mean_data = np.mean(total_data,axis=0)
    return mean_data



total_data = load_data(route='test.jpg', scale=3, index=1, rot_angle=0, start=250,end=800)


# coordinate_set = np.zeros((100, 2))
# for i in range(100):
#     test_data, test_coor = load_data(route='slm_calibration_2/{}.bmp'.format(i+1), scale=3, index=1, rot_angle=0)
#     coordinate_set[i] = test_coor
# print(coordinate_set)

# test_data, test_h = load_data(route='20220628outside.bmp', scale=3, index=1, rot_angle=0)

# test_data, test_w = load_data(route='diff1.png', scale=3, index=1, rot_angle=0)
# print(img_data[:, test_w])
# test = np.array(img_data[:, test_w])

# f = open('result/test1.csv', 'w', encoding='utf-8', newline='')
# csv_write = csv.writer(f)
# for i in range(10):
#   csv_write.writerow(img_data[:, i])

# len_test = img_data.shape
# x_len_test = len_test[0]
#
# x = np.arange(1, x_len_test + 1)
# y = img_data[:, test_w]
# x = np.arange(1, 2689)
# y = img_data[test_h, :]
# plt.title("test plot")
# plt.xlabel("distance")
# plt.ylabel("grayscale")
# plt.plot(x, y)
# plt.show()
# f = open('lumentum_outside.csv', 'w', encoding='utf-8', newline='')
# csv_write = csv.writer(f)
# csv_write.writerow(img_data[test_h, :])
# print(test_coordinate)
# test_data, test_coordinate = load_data(route='slm_calibration/slm_Cali_{}.bmp'.format(seq), scale=3, index=1)

# x = np.arange(1, 1281)
# f = open('20220624/test_1D.csv', 'w', encoding='utf-8', newline='')
# csv_write = csv.writer(f)
# for curDir, dirs, files in os.walk('20220624'):
#     for file in files:
#         if file.endswith(".bmp"):
#             print(os.path.join(curDir, file))
#             test_data, test_h = load_data(route=(os.path.join(curDir, file)), scale=3, index=1, rot_angle=0)
#             img_data = cv2.imread(os.path.join(curDir, file), cv2.IMREAD_GRAYSCALE)
#             csv_write.writerow(img_data[test_h, :])
#             y = img_data[test_h, :]
#             plt.title("test plot")
#             plt.xlabel("distance")
#             plt.ylabel("grayscale")
#             plt.plot(x, y)
#             plt.show()




