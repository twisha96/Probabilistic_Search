from numpy import *
import math
import matplotlib.pyplot as plt
import cell_map as cm
import copy
import pandas as pd

import bonus as bonus
import bonus_part4 as bonusp4

dim = 12
# fig, ax = plt.subplots()
# y_rule1 = []
# y_rule2 = []
# legend = []
column_name_list = ['target_x', ' target_y',
                    'rule 1', 'rule 2', 'rule 3',
                    'rule 1 with travel cost', 'rule 2 with travel cost',
                    'rule 1 utility 1', 'rule 1 utility 2',
                    'rule 2 utility 1', 'rule 2 utility 2']
prob_list = [0.2, 0.3, 0.3, 0.2]
analysis_df = pd.DataFrame(columns=column_name_list)
iterations = 1000
terrain_type_list = [0, 1, 2, 3]
# for terrain_type in terrain_type_list:
cell_map = cm.get_cell_map(dim, prob_list)
# for j in range(dim):
#     for k in range(dim):
for i in range(iterations):
    j = random.randint(0, dim-1)
    k = random.randint(0, dim-1)
    cell_map[j][k].is_target = True
    # x, y, type = cm.add_target(cell_map)
    print "x", j, "y", k, "type", cell_map[j][k].type
    # cm.visualize_board(cell_map)
    print "iteration", i

    search_steps_1, observations_t_1, exec_time_1 = \
        bonus.search_cell_map(copy.deepcopy(cell_map), [], j, k, 0)
    print "Rule 1", search_steps_1, ", exec time: ", exec_time_1
    search_steps_2, observations_t_2, exec_time_2 = \
        bonus.search_cell_map(copy.deepcopy(cell_map), [], j, k, 1)
    print "Rule 2", search_steps_2, ", exec time: ", exec_time_2
    search_steps_3, observations_t_3, exec_time_3 = \
        bonus.search_cell_map(copy.deepcopy(cell_map), [], j, k, 2)
    print "Rule 3", search_steps_3, ", exec time: ", exec_time_3

    modified_search_steps_r1, modified_observations_t_r1, modified_exec_time_r1 = \
        bonusp4.search_cell_map(copy.deepcopy(cell_map), [], j, k, 0, 1)
    print "Rule 1 with travel: ", modified_search_steps_r1
    modified_search_steps_r2, modified_observations_t_r2, modified_exec_time_r2 = \
        bonusp4.search_cell_map(copy.deepcopy(cell_map), [], j, k, 1, 2)
    print "Rule 2 with travel: ", modified_search_steps_r2

    modified_search_steps_1, modified_observations_t_1, modified_exec_time_1 = \
        bonusp4.search_cell_map(copy.deepcopy(cell_map), [], j, k, 0, 0)
    print "Rule 1 Utility 1 - steps: ", modified_search_steps_1
    modified_search_steps_12, modified_observations_t_12, modified_exec_time_12 = \
        bonusp4.search_cell_map(copy.deepcopy(cell_map), [], j, k, 0, 3)
    print "Rule 1 Utility 2 - steps: ", modified_search_steps_12

    modified_search_steps_2, modified_observations_t_2, modified_exec_time_2 = \
        bonusp4.search_cell_map(copy.deepcopy(cell_map), [], j, k, 1, 0)
    print "Rule 2 Utility 1- steps: ", modified_search_steps_2
    modified_search_steps_22, modified_observations_t_22, modified_exec_time_22 = \
        bonusp4.search_cell_map(copy.deepcopy(cell_map), [], j, k, 1, 3)
    print "Rule 2 Utility 2- steps: ", modified_search_steps_22

    df_entry = pd.DataFrame([(j, k, search_steps_1, search_steps_2, search_steps_3,
                              modified_search_steps_r1, modified_search_steps_r2,
                              modified_search_steps_1, modified_search_steps_12,
                              modified_search_steps_2, modified_search_steps_22)],
                            columns=column_name_list, index=[cell_map[j][k].type])
    # print "df entry", df_entry
    analysis_df = analysis_df.append(df_entry)
    # y_rule1.append(search_steps_1)
    # y_rule2.append(search_steps_2)
    analysis_df.to_csv("bonus_analysis.csv")
    cm.remove_target(cell_map, j, k)
#
# ax.plot(density_array, y_baseline)
# ax.plot(density_array, y_inference)
# legend = ['Baseline', 'Inference']
#
# plt.xlabel('Mine Density')
# plt.ylabel('Avg Score Percentage')
# plt.legend(legend, title = 'Algorithm')
# plt.show()
# analysis_df.to_csv("analysis.csv")
