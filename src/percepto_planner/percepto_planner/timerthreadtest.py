#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import time

class Timertest(Node):
    def __init__(self):
        super().__init__("timerthreadtest")
        self.timer1 = self.create_timer(1.0, self.timer1fn)
        self.timer2 = self.create_timer(1.5, self.timer2fn)


    def timer1fn(self):
        self.get_logger().info("Outside While loop timer1  ")

        # while True:
        #     time.sleep(2.0)
        #     self.get_logger().info("Inside while timer 1")
        

    def timer2fn(self):
        self.get_logger().info("Outside while loop timer2")

        # while True:
        #     time.sleep(1.5)
        #     self.get_logger().info("Inside while timer 2")


def main(args=None):
    rclpy.init(args=args)
    node = Timertest()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
