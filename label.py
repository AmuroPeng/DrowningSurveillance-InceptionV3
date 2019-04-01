#!/usr/bin/ env python
# -*- coding:UTF-8 -*-

import tensorflow as tf
import os
from os.path import join as pjoin
import json

data_dir = r".\test"  # 测试集路径

label_lines = [line.rstrip() for line in tf.gfile.GFile("retrained_labels.txt")]  # 将所有训练的类别名用list保存
# print(label_lines) ---> ['drowning', 'normal']
result = {}

for subfolder_name in os.listdir(data_dir):  # 遍历每个子文件夹
    subfolder_dir = pjoin(data_dir, subfolder_name)  # 子文件夹的路径
    for i in os.listdir(subfolder_dir):  # 遍历每个图片
        image_path = pjoin(subfolder_dir, i)  # 得到每个图片的路径
        image_data = tf.gfile.FastGFile(image_path, 'rb').read()  # 读取图片
        # 解析训练结果数据
        with tf.gfile.FastGFile("retrained_graph.pb", 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name='')
        with tf.Session() as sess:
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')  # 将image_data作为每个图片的数据进行操作
            predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})  # 生成预测数据
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]  # 按置信度排序
            # 输出每个成绩
            result_name = './' + str(subfolder_name) + '/' + str(i)
            result_list = []
            for node_id in top_k:
                human_string = label_lines[node_id]
                score = predictions[0][node_id]
                result_list.append(str('%s (score = %.5f)' % (human_string, score)))
            result[result_name] = result_list
            print(result_name, result_list)
json_str = json.dumps(result, indent=4)
# print(json_str)
with open('test_result.json', 'w') as json_file:
    json_file.write(json_str)
