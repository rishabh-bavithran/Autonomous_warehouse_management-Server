#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import cv2
import pygame
import math
from queue import PriorityQueue


# WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

path_grid = []
path_grid_len = 100000

from pplanner_interfaces.msg import ArucoDataset
from pplanner_interfaces.msg import ArucoData
from pplanner_interfaces.msg import PathGrid
from pplanner_interfaces.msg import PathGridset

class PathPlanning(Node):
	def __init__(self):
		super().__init__("path_planner")
		self.get_logger().info("Path Planning Node has started")
		self.total_robot_count = 1
		self.ROWS = 18
		self.COLUMNS = 32
		self.WIDTH = 1280
		self.HEIGHT = 720
		self.robots_target_list = []
		self.robots_list = ArucoDataset()
		self.last_end_row = None
		self.last_end_column = None
		#self.path_grid = []
		# self.last_start = None
		# self.last_end =  None
		self.initial_robots_list_flag = 0
		for iteration in range(self.total_robot_count):
			robot = {'Robot' : iteration+1, 'Status' : 'Unplanned'}
			self.robots_target_list.append(robot)

		self.robots_list_position = self.create_subscription(ArucoDataset, "robots" , self.callback_latest_robot_pos, 10)


		self.robot_status_list = self.create_subscription(ArucoDataset,
													 "path_planning_data",self.callback_robot_status_list_fn, 10)
		
		self.path_planning_timing = self.create_timer(0.5, self.callback_path_planning_timing)
		self.path_grid_pub = self.create_publisher(PathGridset, "path" , 10)
		self.path_grid_pub_timer = self.create_timer(1,  self.path_grid_pub_fn )

	def path_grid_pub_fn(self):
		global path_grid_len
		global path_grid
		#self.get_logger().info("Timer Test")
		self.get_logger().info("path_grid = " + str(len(path_grid)))
		self.get_logger().info("len path grid var = " + str(path_grid_len))
		if path_grid_len == len(path_grid):
			path_grid_list = PathGridset()
			path_grid_list.path = path_grid
			self.get_logger().info("Path is Publishing")
			self.path_grid_pub.publish(path_grid_list)

	def callback_latest_robot_pos(self, msg):
		if self.total_robot_count == len(msg.dataset):
			self.robots_list = msg

	
	def callback_path_planning_timing(self):
		if self.robots_target_list:
			for i in range(self.total_robot_count):
				robot = self.robots_target_list[i]
				if robot.get('Target') != None: 

					end_row, end_column = robot.get('Target')
					if (end_row != self.last_end_row) or (end_column != self.last_end_column):
						WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT)) 
						pygame.display.set_caption("A* Path Finding Algorithm")
						self.last_end_row = end_row 
						self.last_end_column = end_column

						robot_getting_pos = ArucoData()
						for i in range(self.total_robot_count):
							robot_getting_pos = self.robots_list.dataset[i]
							if robot_getting_pos.id_data == robot.get('Robot_ID'):
								robot_row_pos = robot_getting_pos.y_data 
								robot_column_pos = robot_getting_pos.x_data 
								break

						self.path_planner_fn(WIN, self.WIDTH, self.HEIGHT, end_row, end_column, robot_row_pos, robot_column_pos)
						

	
	def path_planner_fn(self, win, width, height, end_row, end_column, robot_row_pos, robot_column_pos):
		grid = make_grid(self.ROWS, self.COLUMNS, height)
		# robot_pos = start
		destination_pos = grid[end_row][end_column] 
		destination_pos.make_end()

		robot_pos = grid[robot_row_pos][robot_column_pos]
		robot_pos.make_start()

		for row in grid:
			#print(row)
			for spot in row:
				#a,b =spot.get_pos()
				#print(a,b)
				spot.update_neighbors(grid)
				
				
		
		algorithm(lambda: draw(win, grid, self.ROWS, self.COLUMNS, width, height), grid, robot_pos, destination_pos)





	def callback_robot_status_list_fn(self, msg):
		# path_planning_len = len(msg.dataset)
		
		path_planning_set = ArucoData()
		if self.initial_robots_list_flag == 0:		
			while self.initial_robots_list_flag < self.total_robot_count:
				path_planning_set = ArucoData()
				path_planning_set = msg.dataset[self.initial_robots_list_flag]
				robot_id = path_planning_set.id_data
				self.robots_target_list[self.initial_robots_list_flag]['Robot_ID'] = robot_id
				target_column_grid = path_planning_set.x_data
				target_row_grid = path_planning_set.y_data
				self.robots_target_list[self.initial_robots_list_flag]['Target'] = (target_row_grid, target_column_grid)
				# self.get_logger().info("Robot : " + str(robot_id) + "  Target : " + "("  +
				# 			  str(target_row_grid)+ " , " +str(target_column_grid) + ")")
				self.get_logger().info(str(self.robots_target_list[self.initial_robots_list_flag]))
				
				self.initial_robots_list_flag+=1

		
		
	
class Spot:
	def __init__(self, row, col, width, total_rows, total_cols):
		self.row = row
		self.col = col
		self.x = col * width
		self.y = row * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows
		self.total_cols = total_cols

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if (self.row < self.total_rows - 1 and self.col < self.total_cols - 1) and not grid[self.row+1][self.col+1].is_barrier():#DOWN RIGHT CORNER 
	
			self.neighbors.append(grid[self.row+1][self.col+1])

		if (self.row < self.total_rows - 1 and self.col > 0) and not grid[self.row + 1][self.col - 1].is_barrier(): #DOWN LEFT CORNER 
			self.neighbors.append(grid[self.row + 1][self.col - 1])

		if (self.col < self.total_cols - 1 and self.row > 0) and not grid[self.row - 1][self.col + 1].is_barrier():#RIGHT UPPER CORNER 
			self.neighbors.append(grid[self.row - 1][self.col + 1])

		if (self.col > 0 and self.row > 0) and not grid[self.row - 1][self.col - 1].is_barrier(): #LEFT UPPER CORNER
			self.neighbors.append(grid[self.row - 1][self.col - 1])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_cols - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])


	def __lt__(self, other):
		return False


def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	#return abs(x1 - x2) + abs(y1 - y2)
	return math.sqrt((abs(x1 - x2))**2 + (abs(y1 - y2))**2)

def reconstruct_path(came_from, current, draw):
	global path_grid_len
	global path_grid
	while current in came_from:
		current = came_from[current]
		row, col = current.get_pos()
		path_coordinate = PathGrid()
		path_coordinate.row = row 
		path_coordinate.col = col 
		path_grid.append(path_coordinate)
		current.make_path()
		draw()
	path_grid.reverse()
	path_grid_len = len(path_grid)
	#print("path_grid = ", path_grid)
	#print("")
	#path_obj = PathPlanning()
	#path_obj.path_grid_pub.publish(path_grid)


def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False


def make_grid(rows, cols, height):
	grid = []
	gap = height // rows
	for i in range(rows):
		grid.append([])
		#print("Doing ROWS")
		for j in range(cols):
			#print("DOing Columns" , j)
			spot = Spot(i, j, gap, rows, cols)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, cols, width, height):
	gap = height // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
	for j in range(cols):
		pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, height))


def draw(win, grid, rows, cols,  width, height):
	win.fill(WHITE)
#VERIFIED THAT THE SPOTS HAVE ALL BEEN MADE INITiALLy
	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, cols, width, height)
	pygame.display.update()


def get_clicked_pos(pos, rows, width , height):
	gap = height // rows
	x, y = pos
	#print(x, y)
	row = y // gap
	col = x // gap

	#print("ROW : ", row)
	#print("COL : ", col)

	return row, col



def main(args=None):
    rclpy.init(args=args)
    node = PathPlanning()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
