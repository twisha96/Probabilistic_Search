import numpy as np
import matplotlib.pyplot as plt

# set width of bar
barWidth = 0.25

# set height of bar
bars1 = [96.76555024, 188.8473054, 229.8034682, 308.5945946]
bars2 = [38.18660287, 92.51197605, 232.1560694, 463.018018]
bars3 = [81.66028708, 177.757485, 253.4393064, 298.6306306]
# bars4 = [104.6507177, 181.6137725, 253.5317919, 342.2792793]
# bars5 = [40.32535885, 92.9011976, 215.5028902, 483.5945946]
# bars6 = [36.29665072, 101.0958084, 215.7398844, 476.8468468]


# Set position of bar on X axis
r1 = np.arange(len(bars1))
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]
# r4 = [x + barWidth for x in r3]
# r5 = [x + barWidth for x in r4]
# r6 = [x + barWidth for x in r5]

# Make the plot
plt.bar(r1, bars1, color='#7f6d5f', width=barWidth, edgecolor='white', label='Rule 1')
plt.bar(r2, bars2, color='#557f2d', width=barWidth, edgecolor='white', label='Rule 2')
plt.bar(r3, bars3, color='#2d7f5e', width=barWidth, edgecolor='white', label='Rule 3')
# plt.bar(r4, bars4, color='lightslategray', width=barWidth, edgecolor='white', label='Rule 1 with Utility 2')
# plt.bar(r5, bars5, color='rosybrown', width=barWidth, edgecolor='white', label='Rule 2 with Utility 1')
# plt.bar(r6, bars6, color='cadetblue', width=barWidth, edgecolor='white', label='Rule 2 with Utility 2')


# Add xticks on the middle of the group bars
plt.xlabel('Terrain', fontweight='bold')
plt.ylabel('Avg Search Steps', fontweight='bold')
plt.xticks([r + barWidth for r in range(4)], ['Flat', 'Hilly', 'Forested', 'Maze of Caves'])

# Create legend & Show graphic
plt.legend()
plt.show()
