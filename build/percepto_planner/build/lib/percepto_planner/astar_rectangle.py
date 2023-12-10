import pygame
import math
from queue import PriorityQueue

WIDTH = 1280
HEIGHT = 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Path Finding Algorithm")

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

		# if self.col < self.total_cols - 1 and not grid[self.row][self.col + 1].is_barrier(): #DOWN
		# 	print("Checking Down")
		# 	self.neighbors.append(grid[self.row][self.col + 1])

		# if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # UP
		# 	print("Checking Up")
		# 	self.neighbors.append(grid[self.row][self.col - 1])

		# if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # RIGHT
		# 	print("Checking Right")
		# 	self.neighbors.append(grid[self.row + 1][self.col])

		# if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # LEFT
		# 	print("Checking Left")
		# 	self.neighbors.append(grid[self.row - 1][self.col])


	def __lt__(self, other):
		return False


def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	#return abs(x1 - x2) + abs(y1 - y2)
	return math.sqrt((abs(x1 - x2))**2 + (abs(y1 - y2))**2)

def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()


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
		print("Doing ROWS")
		for j in range(cols):
			print("DOing Columns" , j)
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
	print(x, y)
	row = y // gap
	col = x // gap

	print("ROW : ", row)
	print("COL : ", col)

	return row, col


def main(win, width , height):
	ROWS = 18
	COLUMNS = 32
	grid = make_grid(ROWS, COLUMNS, height)
	#print(grid)
	start = None
	end = None

	run = True
	while run:
		draw(win, grid, ROWS, COLUMNS, width , height)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				print(pos)
				row, col = get_clicked_pos(pos, ROWS, width, height)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width, height)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						print(row)
						for spot in row:
							a,b =spot.get_pos()
							print(a,b)
							spot.update_neighbors(grid)


					algorithm(lambda: draw(win, grid, ROWS, COLUMNS, width, height), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()

main(WIN, WIDTH ,HEIGHT)