import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

rules = ('Rule 1', 'Rule 2', 'Rule 3')
y_pos = [0.5*x for x in range(len(rules))]
x_pos = [0.5*x+0.15 for x in range(len(rules))]
performance = [6543.154722, 5455.304701, 4985.867063]

plt.bar(y_pos, performance, align='edge', width=0.3, color=('#7f6d5f', '#557f2d', '#2d7f5e'))

plt.xticks(x_pos, rules)
plt.ylabel('Avg Search Steps')

plt.show()