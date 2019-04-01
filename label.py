#!/usr/bin/ env python
# -*- coding:UTF-8 -*-

import tensorflow as tf
import os
from os.path import join as pjoin

data_dir = r".\test"  # 测试集路径

label_lines = [line.rstrip() for line in tf.gfile.GFile("retrained_labels.txt")]  # 删除训练生成的txt文件最后的空格
for subfolder_name in os.listdir(data_dir):
    result_list = []
    result = {}
    subfolder_dir = pjoin(data_dir, subfolder_name)  # 子文件夹的路径
    for i in os.listdir(subfolder_dir):
        image_path = pjoin(subfolder_dir, i)  # 得到每个图片的路径
        image_data = tf.gfile.FastGFile(image_path, 'rb').read()  # 读取图片
        with tf.gfile.FastGFile("retrained_graph.pb", 'rb') as f:  # 解析训练结果数据
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name='')
        with tf.Session() as sess:
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')  # 将image_data作为每个图片的数据进行操作
            predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})  # 生成预测数据
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]  # 按置信度排序
            # 输出每个成绩
            print('文件夹：'+str(subfolder_name)+' 图片：'+str(i))
            for node_id in top_k:
                human_string = label_lines[node_id]
                score = predictions[0][node_id]
                print('%s (score = %.5f)' % (human_string, score))
