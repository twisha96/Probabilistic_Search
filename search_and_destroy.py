import random
import cell_map as cm
import time


def get_not_found_prob(cell_map, cell_cords):
    cell = cell_map[cell_cords[0]][cell_cords[1]]
    return (1-cell.initial_probability) + cell.initial_probability*cell.false_negative


def update_belief_old(cell_map, new_cell, rule_no):
    dim = len(cell_map)
    explored_cell = cell_map[new_cell[0]][new_cell[1]]
    max_belief = 0
    for row in range(0, dim):
        for col in range(0, dim):
            cell = cell_map[row][col]
            if row == new_cell[0] and col == new_cell[1]:
                updated_belief = float(explored_cell.belief*explored_cell.false_negative) / \
                                 float(explored_cell.belief*explored_cell.false_negative + 1 - explored_cell.belief)
                explored_cell.belief = updated_belief

            else:
                explored_cell_not_found_prob = get_not_found_prob(cell_map, new_cell) # not fj
                conditional_not_found_prob = float(explored_cell_not_found_prob - cell.initial_probability)/\
                                             float(1-cell.initial_probability)
                updated_belief = cell.belief/(cell.belief+(1-cell.belief)*conditional_not_found_prob)
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

    max_belief_pool = []
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

    max_belief_pool = []
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


def query_cell(cell_map, cell_location):
    cell = cell_map[cell_location[0]][cell_location[1]]
    if cell.is_target:
        find_target = random.uniform(0, 1)
        false_negative_prob = cell.false_negative
        if find_target >= false_negative_prob:
            return True
    return False


def search_cell_map(cell_map, observations_t, rule_no):
    dim = len(cell_map)
    search_steps = 0
    start_time = time.time()
    max_belief_pool = []
    for i in range(0, dim):
        for j in range(0, dim):
            max_belief_pool.append((i, j))

    while True:
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
        max_belief_pool = update_belief(cell_map, random_cell, rule_no)
        # cm.visualize_probability(cell_map)


# Test code
# prob_list = [0.2, 0.3, 0.3, 0.2]
# dim = 3
# observations_t = []
#
# # cell_map, target_cord_x, target_cord_y, terrain_type = cm.get_cell_map(dim, prob_list)
# cell_map = cm.get_cell_map(dim, prob_list)
# target_cord_x, target_cord_y, terrain_type = cm.add_target(cell_map)
# print "Target location:", target_cord_x, target_cord_y
# print "Target terrain type:", terrain_type
#
# cm.visualize_board(cell_map)
# start_time = time.time()
# search_steps, observations_t, exec_time = search_cell_map(cell_map, observations_t, 0)
# print search_steps

