import random
import cell_map as cm
import time


def get_not_found_prob(cell_map, cell_cords):
    cell = cell_map[cell_cords[0]][cell_cords[1]]
    return (1-cell.initial_probability) + cell.initial_probability * cell.false_negative


def update_belief_using_neighbors(cell_map):
    dim = len(cell_map)
    
    for row in range(dim):
        for col in range(dim):
            updated_belief = 0
            neighbors = cm.get_neighbors(cell_map, row, col)
            for neighbor in neighbors:
                num_neighbors_of_neighbor = len(cm.get_neighbors(cell_map, neighbor[0], neighbor[1]))
                updated_belief += cell_map[neighbor[0]][neighbor[1]].belief * 1.0/num_neighbors_of_neighbor
            cell_map[row][col].belief = updated_belief


def get_p_tracker_out_given_in_cell(cell_terrain, tracker_output):
    if cell_terrain == tracker_output:
        return 0
    return 1.0/3


def get_p_tracker_out_given_not_in_cell(cell_map, cell_terrain, terrain_count, tracker_output):
    dim = len(cell_map)
    total_cells = dim * dim
    if cell_terrain == tracker_output:
        return 1.0/3 * (total_cells - terrain_count[tracker_output]) / (total_cells - 1)
    return 1.0/3 * (total_cells - terrain_count[tracker_output] - 1) / (total_cells - 1)


def update_belief_using_tracker(cell_map, terrain_count, tracker_output, rule_no):
    dim = len(cell_map)
    max_belief = 0
    max_belief_pool = []

    for row in range(dim):
        for col in range(dim):
            cell = cell_map[row][col]
            cell_terrain = cell.type
            p_tracker_out_given_in_cell = get_p_tracker_out_given_in_cell(cell_terrain, tracker_output)
            p_tracker_out_given_not_in_cell = get_p_tracker_out_given_not_in_cell(cell_map, cell_terrain, terrain_count, tracker_output)

            numerator = cell.belief * p_tracker_out_given_in_cell
            denominator = (cell.belief * p_tracker_out_given_in_cell) + ((1 - cell.belief) * p_tracker_out_given_not_in_cell)
            updated_belief = numerator / denominator

            cell.belief = updated_belief

            if rule_no == 1:
                if cell.belief*(1-cell.false_negative) > max_belief:
                    max_belief = cell.belief*(1-cell.false_negative)

            else:
                if cell.belief > max_belief:
                    max_belief = cell.belief

    for row in range(0, dim):
        for col in range(0, dim):
            cell = cell_map[row][col]
            if rule_no == 1:
                if max_belief == cell.belief*(1-cell.false_negative):
                    max_belief_pool.append((row, col))
            else:
                if max_belief == cell.belief:
                    max_belief_pool.append((row, col))            

    return max_belief_pool


def update_belief(cell_map, new_cell, rule_no):
    dim = len(cell_map)
    explored_cell = cell_map[new_cell[0]][new_cell[1]]
    max_belief = 0

    denominator = 0
    for row in range(0, dim):
        for col in range(0, dim):
            cell = cell_map[row][col]
            if row == new_cell[0] and col == new_cell[1]:
                denominator += cell.belief * cell.false_negative
            else:
                denominator += cell.belief

    for row in range(0, dim):
        for col in range(0, dim):
            cell = cell_map[row][col]
            if row == new_cell[0] and col == new_cell[1]:
                updated_belief = float(cell.belief * cell.false_negative)/denominator
                cell.belief = updated_belief
            else:
                updated_belief = float(cell.belief)/denominator
                cell.belief = updated_belief

            if rule_no == 1:
                if max_belief < cell.belief*(1-cell.false_negative):
                    max_belief = cell.belief*(1-cell.false_negative)
            else:
                if max_belief < cell.belief:
                    max_belief = cell.belief

    # prob_map, sum_prob = cm.probability_sanity_check(cell_map)
    # print "prob_map", prob_map
    # print "sum_prob", sum_prob
    # return max_belief_pool


def query_cell(cell_map, cell_location):
    cell = cell_map[cell_location[0]][cell_location[1]]
    if cell.is_target:
        find_target = random.uniform(0, 1)
        false_negative_prob = cell.false_negative
        if find_target >= false_negative_prob:
            return True
    return False


def search_cell_map(cell_map, observations_t, target_cord_x, target_cord_y, rule_no):
    dim = len(cell_map)
    search_steps = 0
    start_time = time.time()
    max_belief_pool = []
    terrain_count = [0, 0, 0, 0]

    for i in range(0, dim):
        for j in range(0, dim):
            max_belief_pool.append((i, j))
            terrain_type = cell_map[i][j].type
            terrain_count[terrain_type] += 1

    while True:
        tracker_output = cm.get_terrain(cell_map, (target_cord_x, target_cord_y))
        # Step C - Update belief based on terrain information from tracker
        max_belief_pool = update_belief_using_tracker(cell_map, terrain_count, tracker_output, rule_no)

        search_steps += 1
        flag = False
        if rule_no == 2:
            for terrain_type in range(4):
                if flag:
                    break
                for i, cell in enumerate(max_belief_pool):
                    if cell_map[cell[0]][cell[1]].type == terrain_type:
                        random_cell = cell
                        # new_pool = [cell]
                        # for j in range(i+1, len(max_belief_pool)):
                        #     cords = max_belief_pool[j]
                        #     if cell_map[cords[0]][cords[1]].type == terrain_type:
                        #         new_pool.append(cords)
                        # random_cell_cords = new_pool[random.randint(0, len(new_pool)-1)]
                        # random_cell = cell_map[random_cell_cords[0]][random_cell_cords[1]]
                        flag = True
                        break
        else:
            n = len(max_belief_pool)
            random_cell_index = 0
            if n > 1:
                random_cell_index = random.randint(0, n-1)
            random_cell = max_belief_pool[random_cell_index]
            # random_cell = max_belief_pool[0]
        observations_t.append((random_cell, cell_map[random_cell[0]][random_cell[1]].belief,
                               cell_map[random_cell[0]][random_cell[1]].type))
        target_found = query_cell(cell_map, random_cell)
        if target_found:
            return search_steps, observations_t, time.time() - start_time

        # Step D - Update belief based on query output of a cell
        update_belief(cell_map, random_cell, rule_no)
        target_cord_x, target_cord_y = cm.move_target(cell_map, (target_cord_x, target_cord_y))
        
        # Step B - After moving target, compute P(in i @ t+1) using P(in neighbor of i @ t)
        update_belief_using_neighbors(cell_map)
        # cm.visualize_probability(cell_map)


# Test code
# prob_list = [0.2, 0.3, 0.3, 0.2]
# dim = 20
# observations_t = []
#
# # cell_map, target_cord_x, target_cord_y, terrain_type = cm.get_cell_map(dim, prob_list)
# cell_map = cm.get_cell_map(dim, prob_list)
# target_cord_x, target_cord_y, terrain_type = cm.add_target(cell_map)
# print "Target location:", target_cord_x, target_cord_y
# print "Target terrain type:", terrain_type
#
# # cm.visualize_board(cell_map)
# start_time = time.time()
# search_steps, observations_t, exec_time = search_cell_map(cell_map, observations_t, target_cord_x, target_cord_y, 0)
# print search_steps

