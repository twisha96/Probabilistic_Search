import random
import game_board as gb
import time


def get_not_found_prob(cell_cords):
    cell = cell_map[cell_cords[0]][cell_cords[1]]
    return (1-cell.initial_probability) + cell.initial_probability*cell.false_negative


def update_belief(cell_map, new_cell, rule_no):
    explored_cell = cell_map[new_cell[0]][new_cell[1]]
    max_belief = 0
    for row in range(0, dim):
        for col in range(0, dim):
            cell = cell_map[row][col]
            if row == new_cell[0] and col == new_cell[1]:
                updated_belief = (float)(explored_cell.p_target*explored_cell.false_negative)/(float)(explored_cell.p_target*explored_cell.false_negative + 1 - explored_cell.p_target)
                explored_cell.p_target = updated_belief

            else:
                explored_cell_not_found_prob = get_not_found_prob(new_cell) # not fj
                conditional_not_found_prob = (float)(explored_cell_not_found_prob - cell.initial_probability)/(float)(1-cell.initial_probability)
                updated_belief = cell.p_target/(cell.p_target+(1-cell.p_target)*conditional_not_found_prob)
                cell.p_target = updated_belief

            if rule_no == 0:
                if max_belief < cell.p_target:
                    max_belief = cell.p_target
            else:
                if max_belief < cell.p_target*(1-cell.false_negative):
                    max_belief = cell.p_target*(1-cell.false_negative)
    max_belief_pool = []
    for row in range(0, dim):
        for col in range(0, dim):
            cell = cell_map[row][col]
            if rule_no == 0:
                if max_belief == cell.p_target:
                    max_belief_pool.append((row, col))
            else:
                if max_belief == cell.p_target*(1-cell.false_negative):
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


def search_cell_map(cell_map, observations_t, max_belief_pool, rule_no):

    search_steps = 0
    while True:
        search_steps += 1
        n = len(max_belief_pool)
        random_cell_index = 0
        if n > 1:
            random_cell_index = random.randint(0, n-1)
        random_cell = max_belief_pool[random_cell_index]
        observations_t.append((random_cell, cell_map[random_cell[0]][random_cell[1]].p_target))
        target_found = query_cell(cell_map, random_cell)
        if target_found:
            return search_steps
        max_belief_pool = update_belief(cell_map, random_cell, rule_no)
        # gb.visualize_probability(cell_map)


# Test code
prob_list = [0.2, 0.3, 0.3, 0.2]
dim = 20
observations_t = []

max_belief_pool = []
for i in range(0, dim):
    for j in range(0, dim):
        max_belief_pool.append((i, j))

cell_map = gb.get_cell_map(dim, prob_list)
(target_cord_x, target_cord_y) = gb.add_target(cell_map)
print "Target location:", target_cord_x, target_cord_y
print "Target terrain type:", cell_map[target_cord_x][target_cord_y].type

# gb.visualize_board(cell_map)
start_time = time.time()
print search_cell_map(cell_map, observations_t, max_belief_pool, 0)
print time.time() - start_time
