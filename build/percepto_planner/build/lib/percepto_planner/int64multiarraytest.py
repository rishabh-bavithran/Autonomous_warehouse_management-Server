#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64MultiArray 

randi = Int64MultiArray()

randi_temp = [(69, 420, 82), (292, 20, 29)]

randi = randi_temp 
