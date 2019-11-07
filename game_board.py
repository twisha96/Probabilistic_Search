import random
from cell import Cell

# import the visualization libraries
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


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
	cell_map = [[Cell() for i in range(dim)] for j in range(dim)]
	cumulative_prob_list = []

	# compute cumulative probability list
	cumulative_prob_list[0] = prob_list[0]
	for i in range(len(prob_list)-1):
		cumulative_prob_list[i+1] = cumulative_prob_list[i] + prob_list[i+1]
						
	# assign terrain type to each cell in the map
	for row in range(dim):
		for col in range(dim):
			random_num = random.uniform(0, 1)
			for terrain_type, prob in enumerate(cumulative_prob_list):
				if random_num<prob:
					cell_map[row][col].type = terrain_type
	target_location = random.randint(0, dim*dim)
	cell_map[target_location/dim][target_location%dim].is_target = True
	 
	return cell_map


# visualises the underlying game board generated
def visualize_board(board):
	basic_board = []
	dim = len(board)

	for i in range(dim):
		basic_board.append([])
		for j in range(dim):
			if board[i][j].is_mine:
				basic_board[i].append(10)
			else:
				basic_board[i].append(board[i][j].clue)

	
	# ax = sns.heatmap(round(corr,2), annot=True, ax=ax, cmap="coolwarm",fmt='.2f', linewidths=.1, linecolor="Black")
	ax = sns.heatmap(basic_board, annot=True, cmap="Blues", cbar=False, linewidths=.1, linecolor="Black")
	plt.show()
	plt.close()


def visualize_board_hidden_cells():
	basic_board = []
	dim = len(board)
	for i in range(dim):
		basic_board.append([])
		for j in range(dim):
			basic_board[i].append(board[i][j].hidden_squares)

	# ax = sns.heatmap(round(corr,2), annot=True, ax=ax, cmap="coolwarm",fmt='.2f', linewidths=.1, linecolor="Black")
	ax = sns.heatmap(basic_board, annot=True, cmap="Blues", cbar=False, linewidths=.1, linecolor="Black")
	plt.show()
	plt.close()

# visualises the current game board as seen by the agent
def visualize_agent_board(board):
	basic_board = []
	dim = len(board)

	for i in range(dim):
		basic_board.append([])
		for j in range(dim):
			if board[i][j].value==-1:
				basic_board[i].append(-1)
			else:
				if board[i][j].is_mine:
					basic_board[i].append(10)
				else:
					basic_board[i].append(board[i][j].clue)
					
	# ax = sns.heatmap(round(corr,2), annot=True, ax=ax, cmap="coolwarm",fmt='.2f', linewidths=.1, linecolor="Black")
	ax = sns.heatmap(basic_board, annot=True, cmap="Blues", cbar=False, linewidths=.1, linecolor="Black")
	plt.show()
	plt.close()
'''
# Test code
game_board = get_board(5,10)
visualize_board(game_board)
'''