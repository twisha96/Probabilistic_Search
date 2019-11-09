import random
from cell import Cell

# import the visualization libraries
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.colors import ListedColormap
import numpy as np


# returns a list of 4 neighbors around a given cell
def get_neighbors(board, x, y):
	dim = len(board)
	neighbor_coordinates = []
	if(y-1>=0):
		neighbor_coordinates.append((x, y-1))
	if(y+1<=dim-1):
		neighbor_coordinates.append((x, y+1))	
	if(x-1>=0):
		neighbor_coordinates.append((x-1, y))
	if(x+1<=dim-1):
		neighbor_coordinates.append((x+1, y))

	return neighbor_coordinates

# returns cell map with dimension dim with n mines
def get_cell_map(dim, prob_list):
	false_negative = {
		0: 0.1,
		1: 0.3,
		2: 0.7,
		3: 0.9
	}
	cell_map = [[Cell() for i in range(dim)] for j in range(dim)]
	cumulative_prob_list = []
	# compute cumulative probability list
	cumulative_prob_list.append(prob_list[0])
	for i in range(len(prob_list)-1):
		cumulative_prob_list.append(cumulative_prob_list[i] + prob_list[i+1])
						
	# assign terrain type to each cell in the map
	for row in range(dim):
		for col in range(dim):
			random_num = random.uniform(0, 1)
			for terrain_type, prob in enumerate(cumulative_prob_list):
				if random_num<prob:
					cell_map[row][col].type = terrain_type
					cell_map[row][col].false_negative = false_negative[cell_map[row][col].type]
					break
	target_location = random.randint(0, dim*dim-1)
	cell_map[target_location/dim][target_location%dim].is_target = True

	return cell_map


def visualize_board(cell_map):
	basic_map = []
	dim = len(cell_map)

	for i in range(dim):
		basic_map.append([])
		for j in range(dim):
			basic_map[i].append(cell_map[i][j].type)
			if cell_map[i][j].is_target:
				target_cords = (i, j)
	draw_board(basic_map, target_cords[0], target_cords[1])


def draw_board(basic_map, i, j):
	cmap = matplotlib.colors.ListedColormap(['silver', 'white', 'forestgreen', 'darkslategray'])
	bounds = [0, 1, 2, 3, 4]
	norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)
	fig, ax = plt.subplots()
	ax.imshow(basic_map, cmap=cmap, norm=norm)
	ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=1)
	ax.set_xticks(np.arange(-.5, dim, step=1));
	ax.set_yticks(np.arange(-.5, dim, step=1));
	ax.text(i, j, 'X', color='red', fontsize=20)
	plt.show()


# Test code
prob_list = [0.2, 0.3, 0.3, 0.2]
dim = 10
cell_map = get_cell_map(dim, prob_list)
visualize_board(cell_map)
