import random
from cell import Cell

# import the visualization libraries
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def assign_hidden_squares_to_edge_cells(board, dim):
	if dim > 1:
		for index in xrange(1, dim-1):
			cell = board[index][0]
			cell.hidden_squares = 5
			cell.no_of_neigbors = 5
			cell = board[index][dim-1]
			cell.hidden_squares = 5
			cell.no_of_neigbors = 5
			cell = board[0][index]
			cell.hidden_squares = 5
			cell.no_of_neigbors = 5
			cell = board[dim-1][index]
			cell.hidden_squares = 5
			cell.no_of_neigbors = 5

def assign_hidden_squares_to_corner_cells(board, dim):
	cell = board[0][0]
	cell.hidden_squares = 3
	cell.no_of_neigbors = 3
	cell = board[0][dim-1]
	cell.hidden_squares = 3
	cell.no_of_neigbors = 3
	cell = board[dim-1][0]
	cell.hidden_squares = 3
	cell.no_of_neigbors = 3
	cell = board[dim-1][dim-1]
	cell.hidden_squares = 3
	cell.no_of_neigbors = 3

def get_knowledge_base_open_safe_cells(board, dim):
	print "Knowlege Base: "
	for i in range(dim):
		for j in range(dim):
			cell = board[i][j]
			if cell.value==0 and (cell.set_value!=0 or (cell.set_value==0 and len(cell.set_of_unknown_neighbors)!=0)):
				print i,j," set: ", sorted(cell.set_of_unknown_neighbors), cell.set_value

def get_knowledge_base(board, dim, set_of_all, set_value):
	get_knowledge_base_open_safe_cells(board, dim)
	print "Board knowledge: ", sorted(set_of_all), set_value

# returns a list of 8 neighbors around a given cell
def get_neighbors(board, x, y):
	dim = len(board)
	neighbor_coordinates = []
	if(y-1>=0):
		neighbor_coordinates.append((x, y-1))
	if(y+1<=dim-1):
		neighbor_coordinates.append((x, y+1))	

	if(x-1>=0):
		neighbor_coordinates.append((x-1, y))
		if(y-1>=0):
			neighbor_coordinates.append((x-1, y-1))
		if(y+1<=dim-1):
			neighbor_coordinates.append((x-1, y+1))

	if(x+1<=dim-1):
		neighbor_coordinates.append((x+1, y))
		if(y-1>=0):
			neighbor_coordinates.append((x+1, y-1))
		if(y+1<=dim-1):
			neighbor_coordinates.append((x+1, y+1))

	return neighbor_coordinates

# returns board with dimension dim with n mines
def get_board(dim, n):
	board = [[Cell() for i in range(dim)] for j in range(dim)]
	
	# this is return a list of n numbers that are locations of mines
	# indexed in row-wise manner
	mine_index = random.sample(range(dim*dim), n)
	# print mine_index
	# get the coordinates x and y using the position index
	mine_locations = []
	for mine_location in mine_index:
		row = mine_location/dim
		col = mine_location%dim
		board[row][col].is_mine = True
		mine_locations.append((row, col))
	
	# get the neighbors of the mine cells and update the clue value
	for mine_location in mine_locations:
		row = mine_location[0]
		col = mine_location[1]
		neighbors = get_neighbors(board, row, col)
		# print row, col, neighbors
		for neighbor in neighbors:
			neighbor_cell = board[neighbor[0]][neighbor[1]]
			if not neighbor_cell.is_mine:
				neighbor_cell.clue += 1

	for row_index in range(0, dim):
		for col_index in range(0, dim):
			cell = board[row_index][col_index]
			neighbors = get_neighbors(board, row_index, col_index)
			cell.set_of_unknown_neighbors = set(neighbors)

	assign_hidden_squares_to_corner_cells(board, dim)
	assign_hidden_squares_to_edge_cells(board, dim)
	
	return board


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