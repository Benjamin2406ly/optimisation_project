import matplotlib.pyplot as plt
import Position
import Delivery

class robot:    
    def __init__(self, position, dir, index, item, color):
        # position.x: 0.25,
        # position.y: -0.75,
        # dir: 'up',
        # index: 0   
        # occupied: False
        self.position = Position.position(position[0], position[1])
        self.position.robot = self 
        self.dir = dir
        self.index = index
        self.item = item
        self.color = color
        self.in_task = False

    def move(self):
        if self.dir == 'up':
            if self.position.y < 8 and 0 < self.position.x < 8:  # 在虚线范围内才能向上移动
                self.position.y += 1
        elif self.dir == 'down':
            if self.position.y > 0 and 0 < self.position.x < 8:  # 在虚线范围内才能向下移动
                self.position.y -= 1
        elif self.dir == 'left':
            if self.position.x > 0 and 0 < self.position.y < 8:  # 在虚线范围内才能向左移动
                self.position.x -= 1
        elif self.dir == 'right':
            if self.position.x < 8 and 0 < self.position.y < 8:  # 在虚线范围内才能向右移动
                self.position.x += 1
        elif self.dir == 'stop':
            pass
        
    def set_dir(self, dir):
        self.dir = dir
    
    def set_index(self, index):
        self.index = index
    
    def plt_robot(self,ax):
        ax.add_patch(plt.Rectangle((self.position.x + self.index + 0.25, self.position.y + 0.25),
                0.5, 0.5, color=self.color, alpha = 1))
    
    def plt_label(self,ax):
        ax.text(self.position.x + self.index + 0.25, self.position.y + 0.25, str(self.item),
                ha='center', va='center', color = 'black',fontsize=12)
    
    def position_to_index(self,position):
        if (self.position.x, self.position.y) == position:
            return self.index

    def next_position(self):
        if self.dir == 'up':
            return Position.position(self.position.x, self.position.y + 1)
        elif self.dir == 'down':
            return Position.position(self.position.x, self.position.y - 1)
        elif self.dir == 'left':
            return Position.position(self.position.x - 1, self.position.y)
        elif self.dir == 'right':
            return Position.position(self.position.x + 1, self.position.y)
    
    def catch_delivery(self, delivery):
        self.item = delivery.item
        self.in_task = True
        delivery.robot = self
        delivery.if_catched()

    def send_delivery(self, delivery):
        delivery.robot = None
        self.item = None
        self.in_task = False
