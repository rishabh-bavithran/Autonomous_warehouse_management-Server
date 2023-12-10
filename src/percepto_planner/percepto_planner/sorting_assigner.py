#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from pplanner_interfaces.msg import ArucoDataset
from pplanner_interfaces.msg import ArucoData
import math

class SortingAssigner(Node):
    def __init__(self):
        super().__init__("sorting_assigner")
        self.get_logger().info("Sorting Assigner Node has started")
        self.robots_list = self.create_subscription(ArucoDataset,"robots", self.callback_robots_arucodataset, 10 )
        self.objects_list = self.create_subscription(ArucoDataset, "objects", self.calback_objects_arucodataset, 10)
        self.robots_total_count = 1
        self.objects_total_count = 1
        self.robots_list_global = ArucoDataset()
        self.objects_list_global = ArucoDataset()
        self.robots_list_latest = ArucoDataset()
        self.robots_status = []
        self.objects_status = []
        self.path_planner_data_global = []
        self.path_planner_pub_data = ArucoDataset()
        
        #self.robot_number = []
        self.i = 0
        self.j = 0 
        self.assigning_timer = self.create_timer(0.5, self.assigning_timer_callback)
        self.publish_motion_planner_data = self.create_timer(0.5, self.publishing_coordinates_fmp) #FOR MOTION PLANNER - FMP
        self.path_planner_pub = self.create_publisher(ArucoDataset, "path_planning_data", 10)
        
    def publishing_coordinates_fmp(self):
        if len(self.path_planner_data_global) == self.robots_total_count :
            self.path_planner_pub_data.dataset = self.path_planner_data_global
            self.path_planner_pub.publish(self.path_planner_pub_data)
            
            
    def calback_objects_arucodataset(self,msg):
        if len(msg.dataset) == self.objects_total_count and self.j == 0:
            #self.get_logger().info("Object count has been verified")
            if self.j == 0:
                self.objects_list_global = msg  
                object_status_track = 0
                while object_status_track < self.objects_total_count:
                    self.objects_status.append("Unpicked") 
                    object_status_track += 1
                self.j += 1

    def callback_robots_arucodataset(self ,msg):
        #self.get_logger().info(str(msg.dataset))
        if self.i == 1 and len(msg.dataset) == self.robots_total_count:
            self.robots_list_latest = msg
            iter1 = 0 
            iter2 = 0 
            temp = ArucoData()
            while iter1 < self.robots_total_count:
                while iter2 < self.robots_total_count:
                    if self.robots_list_global.dataset[iter1].id_data == self.robots_list_latest.dataset[iter2].id_data:
                        temp = self.robots_list_latest.dataset[iter1]
                        self.robots_list_latest.dataset[iter1] = self.robots_list_latest.dataset[iter2]
                        self.robots_list_latest.dataset[iter2] = temp
                        break
                    
                    iter2 += 1

                iter1 += 1


        if len(msg.dataset) == self.robots_total_count and self.i == 0:
            #self.get_logger().info("Robot count has been verified")
            if self.i == 0:
                self.robots_list_global = msg  
                self.robots_list_latest = self.robots_list_global
                robot_status_track = 0
                while robot_status_track < self.robots_total_count:
                    self.robots_status.append("Ready") 
                    robot_status_track += 1
                self.i += 1


    def assigning_timer_callback(self):
        if self.robots_list_global.dataset and self.objects_list_global.dataset:
            #self.get_logger().info("Robot list has been assigned once")
            #self.get_logger().info(str(self.robots_list_global))
            #self.get_logger().info(str(self.robots_status))
            if "Ready" in self.robots_status:
                self.get_logger().info("STARTED ASSIGNING ROBOTS TO OBJECTS")
                if "Unpicked" in self.objects_status:
                    robot_ready_index = self.robots_status.index("Ready")
                    object_unpicked_indices = [o for o, x in enumerate(self.objects_status) if x == "Unpicked"]
                    #object_unpicked_index = self.objects_status.index("Unpicked")
                    self.get_logger().info(str(object_unpicked_indices))
                    robot_assignment = ArucoData()
                    object_assignment = ArucoData()
                    assigned_object = ArucoData()

                    robot_assignment = self.robots_list_latest.dataset[robot_ready_index] #USING CAMERA FEED DATA DIRECTLY TO GET LATEST ROBOT POSITION
                    closest_object_distance = 100000

                    for object_unpicked_index in object_unpicked_indices:
                        self.get_logger().info("FINDING CLOSEST DISTANCE")
                        object_assignment = self.objects_list_global.dataset[object_unpicked_index]
                        distance = math.sqrt(abs((robot_assignment.x_data - object_assignment.x_data)**2 + 
                                       (robot_assignment.y_data - object_assignment.y_data)**2))
                        self.get_logger().info("DISTANCE : " + str(distance))

                        if distance < closest_object_distance:
                            self.get_logger().info("Closest Distance Being Updated") 
                            closest_object_distance = distance
                            final_object_index = object_unpicked_index
                            #assigned_object = object_assignment

                    assigned_object = self.objects_list_global.dataset[final_object_index]
                    self.get_logger().info(str(assigned_object))

                    
                    self.get_logger().info("Assignment has been completed")
                    self.get_logger().info("Robot with ID " + str(robot_assignment.id_data) + 
                                           " has been assigned to Object with ID " + str(assigned_object.id_data))
                    self.objects_status[final_object_index] = "RFP" #Ready For Pickup
                    self.get_logger().info("UPDATED OBJECT STATUS : " + str(self.objects_status))
                    self.robots_status[robot_ready_index] = "Occupied"
                    self.get_logger().info("ROBOTS STATUS : " + str(self.robots_status))
                    path_planner_data = ArucoData()
                    path_planner_data.id_data = robot_assignment.id_data 
                    path_planner_data.x_data = assigned_object.x_data 
                    path_planner_data.y_data = assigned_object.y_data
                    

                    self.path_planner_data_global.append(path_planner_data) 
                    


def main(args=None):
    rclpy.init(args=args)
    node = SortingAssigner()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
