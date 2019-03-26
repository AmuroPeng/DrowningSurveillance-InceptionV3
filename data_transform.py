#!/usr/bin/ env python
# -*- coding:UTF-8 -*-

import cv2

vc = cv2.VideoCapture(r'D:\\5Project\\DrowningSurveillance-InceptionV3\\material\\surveillance1.mp4')  # 读入视频文件
c = 1

if vc.isOpened():  # 判断是否正常打开
    print(1)
    rval, img = vc.read()
else:
    rval = False

timeF = 20  # 视频帧计数间隔频率

while rval:  # 循环读取视频帧
    rval, img = vc.read()
    if (c % timeF == 0):  # 每隔timeF帧进行存储操作
        cv2.imwrite(str('D:\\5Project\\DrowningSurveillance-InceptionV3\\material\\surveillance1\\' + str(c) + '.jpg'), img)  # 存储为图像
        print(str(str(c)))
    c = c + 1
    cv2.waitKey(1)
vc.release()