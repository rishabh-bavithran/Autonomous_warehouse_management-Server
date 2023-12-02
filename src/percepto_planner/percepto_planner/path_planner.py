import rclpy
from rclpy.node import Node
import cv2


class PathPlanning(Node):
    def __init__(self):
        super().__init__("path_planner")
        self.get_logger().info("Path Planning Node has started")
        # Start video capture
        cap = cv2.VideoCapture(0)

        
def main(args=None):
    rclpy.init(args=args)
    node = PathPlanning()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
