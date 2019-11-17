import random
import cell_map as cm
import sys
import time


def get_total_cost_helper(cell_map, source_cell_cords, rule_no):
    total_cost = 0
    dim = len(cell_map)
    for row in range(0, dim):
        for col in range(0, dim):
            total_cost += get_cost(cell_map, (row, col), source_cell_cords, rule_no)
    return float(total_cost) / (dim * dim)


def get_total_cost(cell_map, source_cell_cords, rule_no):
    cell = cell_map[source_cell_cords[0]][source_cell_cords[1]]
    neighborhood_cost = get_total_cost_helper(cell_map, source_cell_cords, rule_no)
    return neighborhood_cost + cell.cost


def get_min_second_step_cost(cell_map, source_cell_cords, rule_no):
    cell = cell_map[source_cell_cords[0]][source_cell_cords[1]]
    min_cost = sys.maxint
    dim = len(cell_map)
    for row in range(0, dim):
        for col in range(0, dim):
            curr_cost = get_cost(cell_map, (row, col), source_cell_cords, rule_no)
            if curr_cost < min_cost:
                min_cost = curr_cost
    return min_cost + cell.cost


def get_rule_1_cost(cell_map, destination_cell_cords):
    cell = cell_map[destination_cell_cords[0]][destination_cell_cords[1]]
    return 1 / cell.belief


def get_rule_2_cost(cell_map, destination_cell_cords):
    cell = cell_map[destination_cell_cords[0]][destination_cell_cords[1]]
    return 1.0 / (cell.belief * (1 - cell.false_negative))


def get_cost(cell_map, destination_cell_cords, source_cell_cords, rule_no):
    destination_cell = cell_map[destination_cell_cords[0]][destination_cell_cords[1]]
    if rule_no == 0:
        destination_cost = 1.0 / destination_cell.belief + (abs(destination_cell_cords[0] - source_cell_cords[0]) +
                                                            abs(destination_cell_cords[1] - source_cell_cords[1]))
    else:
        destination_cost = 1.0 / (destination_cell.belief * (1 - destination_cell.false_negative)) + \
                           (abs(destination_cell_cords[0] - source_cell_cords[0]) +
                            abs(destination_cell_cords[1] - source_cell_cords[1]))
    return destination_cost


def get_not_found_prob(cell_map, cell_cords):
    cell = cell_map[cell_cords[0]][cell_cords[1]]
    return (1 - cell.initial_probability) + cell.initial_probability * cell.false_negative


def update_belief(cell_map, new_cell, rule_no, cost_function):
    explored_cell = cell_map[new_cell[0]][new_cell[1]]
    min_cost = sys.maxint
    dim = len(cell_map)

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
                updated_belief = float(cell.belief * cell.false_negative) / denominator
                cell.belief = updated_belief
            else:
                updated_belief = float(cell.belief) / denominator
                cell.belief = updated_belief

    for row in range(0, dim):
        for col in range(0, dim):
            cell = cell_map[row][col]
            cell.cost = get_cost(cell_map, (row, col), (new_cell[0], new_cell[1]), rule_no)

    for row in range(0, dim):
        for col in range(0, dim):
            cell = cell_map[row][col]
            if cost_function == 0:
                cell.utility = cell.cost
            elif cost_function == 1:
                cell.utility = get_rule_1_cost(cell_map, (row, col))
            elif cost_function == 2:
                cell.utility = get_rule_2_cost(cell_map, (row, col))
            elif cost_function == 3:
                cell.utility = get_total_cost(cell_map, (row, col), rule_no)
            elif cost_function == 4:
                cell.utility = get_min_second_step_cost(cell_map, (row, col), rule_no)

            if cell.utility < min_cost:
                min_cost = cell.utility

    min_cost_pool = []
    for row in range(0, dim):
        for col in range(0, dim):
            cell = cell_map[row][col]
            if min_cost == cell.utility:
                min_cost_pool.append((row, col))

    return min_cost_pool


def query_cell(cell_map, cell_location):
    cell = cell_map[cell_location[0]][cell_location[1]]
    if cell.is_target:
        find_target = random.uniform(0, 1)
        false_negative_prob = cell.false_negative
        if find_target >= false_negative_prob:
            return True
    return False


def search_cell_map(cell_map, observations_t, rule_no, cost_function):
    search_steps = 0
    start_time = time.time()
    max_belief_pool = []

    dim = len(cell_map)

    for i in range(0, dim):
        for j in range(0, dim):
            max_belief_pool.append((i, j))

    while True:
        search_steps += 1
        n = len(max_belief_pool)
        random_cell_index = 0
        if n > 1:
            random_cell_index = random.randint(0, n - 1)
        random_cell = max_belief_pool[random_cell_index]

        if search_steps == 1:
            prev_random_cell = random_cell

        # print "before search_steps", search_steps
        search_steps += abs(random_cell[0] - prev_random_cell[0]) + \
                        abs(random_cell[1] - prev_random_cell[1])
        # print "distance cost", abs(random_cell[0] - prev_random_cell[0]) + abs(random_cell[1] - prev_random_cell[1])
        # print "after search_steps", search_steps

        prev_random_cell = random_cell
        observations_t.append((random_cell, cell_map[random_cell[0]][random_cell[1]].belief))
        target_found = query_cell(cell_map, random_cell)
        if target_found:
            return search_steps, observations_t, time.time() - start_time
        max_belief_pool = update_belief(cell_map, random_cell, rule_no, cost_function)
        # cm.visualize_probability(cell_map)

# Test code
prob_list = [0.2, 0.3, 0.3, 0.2]
dim = 12
observations_t = []

max_belief_pool = []
for i in range(0, dim):
    for j in range(0, dim):
        max_belief_pool.append((i, j))

cell_map = cm.get_cell_map(dim, prob_list)
(target_cord_x, target_cord_y, cell_type) = cm.add_target(cell_map)
print "Target location:", target_cord_x, target_cord_y
print "Target terrain type:", cell_map[target_cord_x][target_cord_y].type
# cm.visualize_board(cell_map)

start_time = time.time()
search_steps, observations_t, execution_time = search_cell_map(cell_map, observations_t, 0, 4)
print search_steps
print execution_time
#print "Observations: ", observations_t
#print time.time() - start_time
