import random
import cell_map as cm
import sys
import time


def get_new_cost(cell_map, destination_cell_cords, source_cell_cords, rule_no):
    dim = len(cell_map)
    local_dist = abs(destination_cell_cords[0] - source_cell_cords[0]) + abs(destination_cell_cords[1] - source_cell_cords[1])
    local_cost = local_dist + 1

    explored_cell = cell_map[destination_cell_cords[0]][destination_cell_cords[1]]
    future_discount = 0
    if rule_no == 1:
        future_discount = 1 - explored_cell.belief * (1 - explored_cell.false_negative)
    else:
        future_discount = 1 - explored_cell.belief

      
    denominator = explored_cell.belief * explored_cell.false_negative + (1 - explored_cell.belief)

    future_costs = []
    for row in range(0, dim):
        for col in range(0, dim):
            if row!=destination_cell_cords[0] or col!=destination_cell_cords[1]:
                future_cost = 0
                cell = cell_map[row][col]
                future_dist = abs(row - destination_cell_cords[0]) + abs(col - destination_cell_cords[1])

                updated_belief = 0.0
                if row == destination_cell_cords[0] and col == destination_cell_cords[1]:
                    updated_belief = float(cell.belief * cell.false_negative) / denominator
                else:
                    updated_belief = float(cell.belief) / denominator

                if rule_no == 1:
                    future_cost = future_discount * (2 + future_dist - updated_belief * (1 - cell.false_negative))
                else:
                    future_cost = future_discount * (2 + future_dist - updated_belief)

                future_costs.append(future_cost)

    avg_future_cost = sum(future_costs)/len(future_costs)
    min_future_cost = min(future_costs)
    total_cost = local_cost + min_future_cost
    return total_cost

def update_belief(cell_map, new_cell, rule_no):
    explored_cell = cell_map[new_cell[0]][new_cell[1]]
    min_cost = sys.maxint
    dim = len(cell_map)

    denominator = explored_cell.belief * explored_cell.false_negative + (1 - explored_cell.belief)

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
            if row!=new_cell[0] or col!=new_cell[1]:
                cell = cell_map[row][col]
                cell.new_cost = get_new_cost(cell_map, (row, col), (new_cell[0], new_cell[1]), rule_no)
                if cell.new_cost < min_cost:
                    min_cost = cell.new_cost

    min_cost_pool = []
    for row in range(0, dim):
        for col in range(0, dim):
            cell = cell_map[row][col]
            if min_cost == cell.new_cost:
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


def search_cell_map(cell_map, observations_t, rule_no):
    search_steps = 0
    start_time = time.time()
    max_belief_pool = []

    dim = len(cell_map)

    for i in range(0, dim):
        for j in range(0, dim):
            max_belief_pool.append((i, j))

    while True:
        for row in range(0, dim):
            for col in range(0, dim):
                cell_temp = cell_map[row][col]
                # print row, col, cell_temp.belief
        search_steps += 1
        n = len(max_belief_pool)
        random_cell_index = 0
        if n > 1:
            random_cell_index = random.randint(0, n - 1)
        random_cell = max_belief_pool[random_cell_index]
        # print "cell being queried", random_cell

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
        max_belief_pool = update_belief(cell_map, random_cell, rule_no)
        # cm.visualize_probability(cell_map)

# Test code
# prob_list = [0.2, 0.3, 0.3, 0.2]
# dim = 12
# observations_t = []

# max_belief_pool = []
# for i in range(0, dim):
#     for j in range(0, dim):
#         max_belief_pool.append((i, j))

# cell_map = cm.get_cell_map(dim, prob_list)
# (target_cord_x, target_cord_y, cell_type) = cm.add_target(cell_map)
# print "Target location:", target_cord_x, target_cord_y
# print "Target terrain type:", cell_map[target_cord_x][target_cord_y].type
# #cm.visualize_board(cell_map)

# start_time = time.time()
# search_steps, observations_t, execution_time = search_cell_map(cell_map, observations_t, 1)
# print search_steps
# print execution_time
#print "Observations: ", observations_t
#print time.time() - start_time
