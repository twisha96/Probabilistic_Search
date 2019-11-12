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
    if (y - 1 >= 0):
        neighbor_coordinates.append((x, y - 1))
    if (y + 1 <= dim - 1):
        neighbor_coordinates.append((x, y + 1))
    if (x - 1 >= 0):
        neighbor_coordinates.append((x - 1, y))
    if (x + 1 <= dim - 1):
        neighbor_coordinates.append((x + 1, y))

    return neighbor_coordinates


def remove_target(cell_map, x_cord, y_cord):
    cell_map[x_cord][y_cord].is_target = False


def add_target(cell_map):
    dim = len(cell_map)
    target_location_x = random.randint(0, dim - 1)  #
    target_location_y = random.randint(0, dim - 1)
    cell_map[target_location_x][target_location_y].is_target = True
    return target_location_x, target_location_y, cell_map[target_location_x][target_location_y].type


def get_cell_map(dim, prob_list):
    # initialize the false negative probability based on the terrain type
    false_negative = {
        0: 0.1,
        1: 0.3,
        2: 0.7,
        3: 0.9
    }
    cell_map = [[Cell() for col in range(dim)] for row in range(dim)]
    # compute cumulative probability list
    cumulative_prob_list = [prob_list[0]]
    for i in range(len(prob_list) - 1):
        cumulative_prob_list.append(cumulative_prob_list[i] + prob_list[i + 1])

    # assign terrain type to each cell in the map
    for row in range(dim):
        for col in range(dim):
            cell = cell_map[row][col]
            cell.p_target = 1.0 / (dim * dim)
            cell.initial_probability = 1.0 / (dim * dim)
            # generate random number to assign terrain type to the cell
            random_num = random.uniform(0, 1)
            for terrain_type, prob in enumerate(cumulative_prob_list):
                if random_num < prob:
                    cell.type = terrain_type
                    # print "Cell type: ", cell.type
                    cell.false_negative = false_negative[cell.type]
                    break

    # target_location_x = random.randint(0, dim - 1)
    # target_location_y = random.randint(0, dim - 1)
    # cell_map[target_location_x][target_location_y].is_target = True
    return cell_map#, target_location_x, target_location_y, cell_map[target_location_x][target_location_y].type

def get_specific_cell_map(dim, prob_list, terrain_type_value):
    # initialize the false negative probability based on the terrain type
    false_negative = {
        0: 0.1,
        1: 0.3,
        2: 0.7,
        3: 0.9
    }
    terrain_cell_pool = []
    cell_map = [[Cell() for i in range(dim)] for j in range(dim)]
    # compute cumulative probability list
    cumulative_prob_list = [prob_list[0]]
    for i in range(len(prob_list) - 1):
        cumulative_prob_list.append(cumulative_prob_list[i] + prob_list[i + 1])

    # assign terrain type to each cell in the map
    for row in range(dim):
        for col in range(dim):
            cell = cell_map[row][col]
            cell.p_target = 1.0 / (dim * dim)
            cell.initial_probability = 1.0 / (dim * dim)
            # generate random number to assign terrain type to the cell
            random_num = random.uniform(0, 1)
            for terrain_type, prob in enumerate(cumulative_prob_list):
                if random_num < prob:
                    cell.type = terrain_type
                    cell.false_negative = false_negative[cell.type]
                    if terrain_type == terrain_type_value:
                        terrain_cell_pool.append((row, col))
                    break

    target_location = terrain_cell_pool[random.randint(0, len(terrain_cell_pool)-1)]
    cell_map[target_location[0]][target_location[1]].is_target = True
    return cell_map, target_location[0], target_location[1]


def visualize_probability(cell_map):
    basic_map = []
    dim = len(cell_map)

    for i in range(dim):
        basic_map.append([])
        for j in range(dim):
            basic_map[i].append(cell_map[i][j].p_target)
    ax = sns.heatmap(basic_map, cmap="Blues", cbar=False, linewidths=.1, linecolor="Black", annot=True)
    plt.show()


def probability_sanity_check(cell_map):
    prob = []
    sum = 0.0
    dim = len(cell_map)
    for i in range(dim):
        for j in range(dim):
            curr_prob = cell_map[i][j].p_target
            prob.append(curr_prob)
            sum += curr_prob
    return prob, sum


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
    # dim = len(basic_map)
    # cmap = matplotlib.colors.ListedColormap(['silver', 'white', 'forestgreen', 'darkslategray'])
    # bounds = [0, 1, 2, 3, 4]
    # norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)
    # fig, ax = plt.subplots()
    # ax.imshow(basic_map, cmap=cmap, norm=norm)
    # ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=1)
    # ax.set_xticks(np.arange(0, dim, step=1))
    # ax.set_yticks(np.arange(0, dim, step=1))
    # ax.text(i, j, 'X', color='red', fontsize=20)
    # plt.show()

    colors = ['white', 'silver', 'forestgreen', 'darkslategray']
    cmap = sns.color_palette(colors)
    ax = sns.heatmap(basic_map, annot=False, cmap=cmap, cbar=True,
                     vmax=4, vmin=0, linewidths=.1, linecolor="Black")
    plt.text(i+0.5, j+0.5, 'X', color='red', fontsize=10, horizontalalignment="center", verticalalignment="center")
    plt.show()


# Test code
#
# prob_list = [0.2, 0.3, 0.3, 0.2]
# dim = 10
# cell_map = get_cell_map(dim, prob_list)
# visualize_board(cell_map)
