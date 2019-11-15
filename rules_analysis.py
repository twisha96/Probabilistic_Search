from numpy import *
import math
import matplotlib.pyplot as plt
import cell_map as cm
import copy
import pandas as pd

import search_and_destroy as sd

dim = 3
# fig, ax = plt.subplots()
# y_rule1 = []
# y_rule2 = []
# legend = []
column_name_list = ['search steps 1', 'search steps 2', 'search steps 3', 'exec time 1', 'exec time 2', 'exec time 3']
prob_list = [0.2, 0.3, 0.3, 0.2]
analysis_df = pd.DataFrame(columns=column_name_list)
iterations = 10
terrain_type_list = [0, 1, 2, 3]
# for terrain_type in terrain_type_list:
cell_map = cm.get_cell_map(dim, prob_list)
for j in range(dim):
    for k in range(dim):
        cell_map[j][k].is_target = True
        terrain_type = cell_map[j][k].type
        # x, y, type = cm.add_target(cell_map)
        print "x", j, "y", k, "type", terrain_type
        # cm.visualize_board(cell_map)
        for i in range(iterations):
            print "iteration", i
            search_steps_1, observations_t_1, exec_time_1 = sd.search_cell_map(copy.deepcopy(cell_map), [], 0)
            print "Rule 1- steps: ", search_steps_1, ", exec time: ", exec_time_1
            search_steps_2, observations_t_2, exec_time_2 = sd.search_cell_map(copy.deepcopy(cell_map), [], 1)
            print "Rule 2- steps: ", search_steps_2, ", exec time: ", exec_time_2
            search_steps_3, observations_t_3, exec_time_3 = sd.search_cell_map(copy.deepcopy(cell_map), [], 2)
            print "Rule 3- steps: ", search_steps_3, ", exec time: ", exec_time_3

            df_entry = pd.DataFrame([(search_steps_1, search_steps_2, search_steps_3, exec_time_1,  exec_time_2,
                                      exec_time_3)], columns=column_name_list, index=[terrain_type])

            # print "df entry", df_entry
            analysis_df = analysis_df.append(df_entry)
            # y_rule1.append(search_steps_1)
            # y_rule2.append(search_steps_2)
            analysis_df.to_csv("analysis_6.csv")
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
