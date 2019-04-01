#!/usr/bin/ env python
# -*- coding:UTF-8 -*-

import os
from os.path import join as pjoin
from PIL import Image

data_dir = r".\material\Transformed"  # data_dir是lfw数据集路径
img_dir = r".\material\Tailored"  # 自己单独建的文件夹, 用于存放从lfw读取的图片

for folder_name in os.listdir(data_dir):
    count = 0
    person_dir = pjoin(data_dir, folder_name)  # lfw中文件夹的路径
    for i in os.listdir(person_dir):
        image_dir = pjoin(person_dir, i)  # lfw中每个文件夹中图片的路径
        img = Image.open(image_dir)  # 读取每个图片
        cropped = img.crop((81, 39, 457, 312))  # (left, upper, right, lower)
        cropped.save(pjoin(img_dir, folder_name, i))  # 将lfw中读取的每个文件夹中的图片存入指定的文件夹
        count = count + 1
    print('文件夹 '+str(folder_name) + ' 中有 ' + str(count) + ' 个图片被截取')


