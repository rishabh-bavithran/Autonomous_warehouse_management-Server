#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from pplanner_interfaces.msg import ArucoData
from pplanner_interfaces.msg import ArucoDataset
#from example_interfaces.msg import Float64
import cv2
import cv2.aruco as aruco
import numpy as np


class MyNode(Node):

    def __init__(self):
        super().__init__("visual_feed")
        self.counter_ = 0
        self.get_logger().info("Hello ROS2")
        self.publish_robot_data = self.create_publisher(ArucoDataset,"robots",10)
        self.publish_object_data = self.create_publisher(ArucoDataset,"objects",10)
        self.cap = cv2.VideoCapture(0)
        self.create_timer(0.1, self.camera_feed)
        self.width_frame = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height_frame = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.gap = 40

        self.get_logger().info("WIDTH AND HEIGHT " + str(type(self.width_frame)))    
        self.get_logger().info("wIDTH : " + str(self.width_frame))
        self.get_logger().info("HEIGHT : " + str(self.height_frame))

    def camera_feed(self):
        # Capture frame-by-frame
        ret, frame = self.cap.read()

        if ret:
            
            # Detect ArUco markers
            corners, ids = self.detect_aruco_markers(frame)

            if ids is not None:
                # Annotate frame with marker information
                self.annotate_frame(frame, corners, ids)

                # Get marker information
                marker_info = self.get_marker_info(corners, ids)

                # Sort markers
                even_markers, odd_markers = self.sort_markers(marker_info)


                # robot_data_array = ArucoDataset()
                # object_data_array = ArucoDataset()
                robot_data_array = []
                object_data_array = []
                # while i < len(even_markers):
                #     even_markers[i] = robot_data_array

                # while j < len(even_markers):
                #     object_data_array[j] = robot_data_array


                i=0
                j=0

                while i < len(odd_markers):

                    robot_data = ArucoData()
                    robot_data.id_data = int(odd_markers[i][0])
                    self.get_logger().info(str(robot_data.id_data))
                    robot_data.x_data =  int(odd_markers[i][1]) //self.gap
                    robot_data.y_data =  int(odd_markers[i][2]) //self.gap
                    robot_data.orientation_data =  float(odd_markers[i][3])
                    robot_data_array.append(robot_data)
                    i+=1
                rob_pub = ArucoDataset()
                rob_pub.dataset = robot_data_array
                self.get_logger().info(str(rob_pub))

                while j < len(even_markers): 
                    object_data = ArucoData()
                    object_data.id_data =  int(even_markers[j][0])
                    self.get_logger().info(str(object_data.id_data))
                    object_data.x_data =  int(even_markers[j][1]) // self.gap
                    object_data.y_data =  int(even_markers[j][2]) // self.gap
                    object_data.orientation_data =  float(even_markers[j][3])
                    object_data_array.append(object_data)
                    j+=1

                obj_pub = ArucoDataset()
                obj_pub.dataset = object_data_array
                self.get_logger().info(str(obj_pub))



                self.publish_robot_data.publish(rob_pub)
                self.publish_object_data.publish(obj_pub)






                # print("Even Markers:", even_markers
                # print("Odd Markers:", odd_markers)
                
                #odd_markers_float =  [[float(item) for item in sublist] for sublist in odd_markers]
                #even_markers_float =  [[float(item) for item in sublist] for sublist in even_markers]





            # Display the resulting frame
            cv2.imshow('Frame', frame)
            cv2.waitKey(1)  # Wait for a short time to process GUI events


        else:
            self.get_logger().warning("ret is False")

    def detect_aruco_markers(self, frame):
        # Load the ArUco dictionary
        aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        aruco_params = aruco.DetectorParameters_create()

        # Detect markers
        corners, ids, _ = aruco.detectMarkers(frame, aruco_dict, parameters=aruco_params)

        return corners, ids

    def get_marker_info(self, corners, ids):
        marker_info = []

        for i, corner in enumerate(corners):
            id = ids[i][0]
            # Calculate the center point of the marker
            center_x = int((corner[0][0][0] + corner[0][2][0]) / 2)
            center_y = int((corner[0][0][1] + corner[0][2][1]) / 2)
            # Calculate orientation (this is a placeholder, adjust as needed)
            orientation = np.arctan2(corner[0][1][1] - corner[0][0][1], corner[0][1][0] - corner[0][0][0])
            marker_info.append([id, center_x, center_y, orientation])

        return marker_info

    def sort_markers(self, marker_info):
        even_markers = []
        odd_markers = []

        for info in marker_info:
            if info[0] % 2 == 0:
                even_markers.append(info)
            else:
                odd_markers.append(info)

        return even_markers, odd_markers

    def annotate_frame(self, frame, corners, ids):
        for i, corner in enumerate(corners):
            id = ids[i][0]
            # Determine if the ID is odd or even
            text = 'Odd' if id % 2 else 'Even'

            # Calculate the center point of the marker for text placement
            center_x = int((corner[0][0][0] + corner[0][2][0]) / 2)
            center_y = int((corner[0][0][1] + corner[0][2][1]) / 2)

            # Put text on the frame
            cv2.putText(frame, text, (center_x, center_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)




def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
