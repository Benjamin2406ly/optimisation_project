# from scipy.optimize import linear_sum_assignment    
# import numpy as np

# matrix = np.array([[6, 2, 3], [-1, 5, 6], [7, 8, 5]])

# row_ind, col_ind = linear_sum_assignment(matrix)
# print(row_ind, col_ind)
# print(matrix[row_ind, col_ind].sum())

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

class Robot:
    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir

    def plt_robot(self):
        return plt.Rectangle((self.x, self.y), 1, 1, color='blue')

    def plt_label(self):
        return [self.x + 0.5, self.y + 0.5, 'Robot']
    
    def move(self):
        direction = random.choice(['up', 'down', 'left', 'right'])
        if direction == 'up':
            self.y += 1
        elif direction == 'down':
            self.y -= 1
        elif direction == 'left':
            self.x -= 1
        elif direction == 'right':
            self.x += 1
    
    def set_dir(self, dir):
        self.dir = dir
    
fig,ax = plt.subplots()
square = Robot(0, 0 , 'up')
patchs = []
texts = []
patchs.append(square.plt_robot())
texts.append(square.plt_label())

def update_patch(patchs, texts):
    for patch in patchs:
        patch.set_x(square.x)
        patch.set_y(square.y)
    for txt in ax.texts:
        txt.remove()
    for text in texts:
        text[0]=(square.x + 0.5)
        text[1]=(square.y + 0.5)

def update(frame):
    direction = random.choice(['up', 'down', 'left', 'right'])  
    square.set_dir(direction)
    square.move()
    update_patch(patchs,texts)
    ax.add_patch(patchs[0])
    ax.text(*texts[0], ha = 'center', va = 'center', color = 'black',fontsize = 8)
    return ax,
    

ani = FuncAnimation(fig, update, frames=range(20), interval=200, blit=True)

plt.xlim(-10, 10)
plt.ylim(-10, 10)
plt.show()

# print(square.x, square.y)