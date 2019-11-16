import numpy as np
import matplotlib.pyplot as plt

# set width of bar
barWidth = 0.25

# set height of bar
bars1 = [2627.478261, 5617.285714, 9327.640625, 8600.214286]
bars2 = [904.3695652, 2256.21978, 5142.34375, 13518.28571]
# bars3 = [1440.217391, 4716.659341, 5503.109375, 8283.482143]
# bars4 = [442.7426471, 732.1341853, 1342.98452, 1534.157895]
# bars5 = [163.8455882, 388.2364217, 918.5820433, 2277.614035]
# bars6 = [113.2941176, 443.0319489, 993.9009288, 2587.118421]


# Set position of bar on X axis
r1 = np.arange(len(bars1))
r2 = [x + barWidth for x in r1]
# r3 = [x + barWidth for x in r2]
# r4 = [x + barWidth for x in r3]
# r5 = [x + barWidth for x in r4]
# r6 = [x + barWidth for x in r5]

# Make the plot
plt.bar(r1, bars1, color='#7f6d5f', width=barWidth, edgecolor='white', label='Rule 1')
plt.bar(r2, bars2, color='#557f2d', width=barWidth, edgecolor='white', label='Rule 2')
# plt.bar(r3, bars3, color='#2d7f5e', width=barWidth, edgecolor='white', label='Rule 3')
# plt.bar(r4, bars4, color='lightslategray', width=barWidth, edgecolor='white', label='Rule 1 based Augmented Cost')
# plt.bar(r5, bars5, color='rosybrown', width=barWidth, edgecolor='white', label='Rule 2 based Cost')
# plt.bar(r6, bars6, color='cadetblue', width=barWidth, edgecolor='white', label='Rule 2 based Augmented Cost')


# Add xticks on the middle of the group bars
plt.xlabel('Terrain', fontweight='bold')
plt.ylabel('Avg Search Steps', fontweight='bold')
plt.xticks([r + 0.5*barWidth for r in range(4)], ['Flat', 'Hilly', 'Forested', 'Maze of Caves'])

# Create legend & Show graphic
plt.legend()
plt.show()
