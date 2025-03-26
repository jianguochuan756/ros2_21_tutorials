#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

"""
@作者: 古月居(www.guyuehome.com)
@说明: ROS2节点示例-通过颜色识别检测图片中出现的苹果
"""

import rclpy                            # ROS2 Python接口库
from rclpy.node import Node             # ROS2 节点类

import cv2                              # OpenCV图像处理库
import numpy as np                      # Python数值计算库

#定义 HSV 颜色空间中红色的阈值范围（Hue: 色调，Saturation: 饱和度，Value: 明度）
#np.array([a, b, c])是一个包含 ​3 个元素的一维数组，表示 RGB 或 HSV 颜色空间中的某个颜色值。

lower_red = np.array([0, 90, 128])     # 红色的HSV阈值下限
upper_red = np.array([180, 255, 255])  # 红色的HSV阈值上限

def object_detect(image):
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)                               # 图像从BGR颜色模型转换为HSV模型
    mask_red = cv2.inRange(hsv_img, lower_red, upper_red)                          # 图像二值化;使用 inRange 函数根据阈值提取红色区域，生成黑白二值图像（白色为红色区域）。
    
    #图像中轮廓检测
    contours, hierarchy = cv2.findContours(mask_red, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE) # findContours 检测二值图像中的轮廓。
                                                                                           # RETR_LIST: 检索所有独立轮廓。
                                                                                           # CHAIN_APPROX_NONE: 保存所有轮廓点。


    for cnt in contours:                                                          # 去除一些轮廓面积太小的噪声
        if cnt.shape[0] < 150:
            continue
            
        (x, y, w, h) = cv2.boundingRect(cnt)                                      # 得到苹果所在轮廓的左上角xy像素坐标及轮廓范围的宽和高
        cv2.drawContours(image, [cnt], -1, (0, 255, 0), 2)                        # 将苹果的轮廓勾勒出来
        cv2.circle(image, (int(x+w/2), int(y+h/2)), 5, (0, 255, 0), -1)           # 将苹果的图像中心点画出来
	    
    cv2.imshow("object", image)                                                    # 使用OpenCV显示处理后的图像效果
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main(args=None):                                                              # ROS2节点主入口main函数
    rclpy.init(args=args)                                                         # ROS2 Python接口初始化
    node = Node("node_object")                                                     # 创建ROS2节点对象并进行初始化
    node.get_logger().info("ROS2节点示例：检测图片中的苹果")


# image=cv.imread()从指定路径加载图像文件，并将其转换为 OpenCV 可处理的矩阵格式（NumPy 数组）。
# 成功时：返回一个表示图像的 ​三维 NumPy 数组​（高度 × 宽度 × 通道数）。
# 失败时（如路径错误）：返回 None。
# cv2.imread(filename, flags)
#模式	                值	            说明
#cv2.IMREAD_COLOR	    1	  读取彩色图像（默认），忽略透明度通道（3通道）。
#cv2.IMREAD_GRAYSCALE	0	  以灰度模式读取图像（单通道）。
#cv2.IMREAD_UNCHANGED	-1	  保留原始图像格式（包括 Alpha 通道）。

    image = cv2.imread('/home/dev_sxc/src/ros2_21_tutorials/learning_node/learning_node/apple.jpg')  # 读取图像

    object_detect(image)                                                            # 调用object_detect处理图像——苹果检测
    rclpy.spin(node)                                                               # 循环等待ROS2退出
    node.destroy_node()                                                            # 销毁节点对象
    rclpy.shutdown()                                                               # 关闭ROS2 Python接口
