#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

"""
@作者: 古月居(www.guyuehome.com)
@说明: ROS2节点示例-发布“Hello World”日志信息, 使用面向过程的实现方式
"""

import rclpy                                     # ROS2 Python接口库
from rclpy.node import Node                      # ROS2 节点类  /rclpy.node是rclpy中的一个模块；Node是ROS2节点的基类（Base Class），所有 ROS2 节点都必须继承自此类。
import time

def main(args=None):                             # ROS2节点主入口main函数
    rclpy.init(args=args)                        # ROS2 Python接口初始化
    node = Node("node_helloworld")               # 创建“node_helloworld”节点对象并进行初始化
    
    while rclpy.ok():                            # ROS2系统是否正常运行；持续检测 ROS2 是否存活（如未收到终止信号则返回 True）。
        node.get_logger().info("Hello World")    # ROS2日志输出
        time.sleep(0.5)                          # 休眠控制循环时间，让循环每秒执行两次
    
    node.destroy_node()                          # 销毁节点对象    
    rclpy.shutdown()                             # 关闭ROS2 Python接口
