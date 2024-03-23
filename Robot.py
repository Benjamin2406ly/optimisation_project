import matplotlib.pyplot as plt
import Position
import Delivery

class robot(Position.position):    
    def __init__(self, position, dir, index, item, color):
        # x: 0.25,
        # y: -0.75,
        # dir: 'up',
        # index: 0   
        # occupied: False
        position.__init__(position[0], position[1]) # (x,y)
        position.robot = self 
        self.dir = dir
        self.index = index
        self.item = item
        self.color = color

    def move(self):
        if self.dir == 'up':
            if self.y < 8 and 0 < self.x < 8:  # 在虚线范围内才能向上移动
                self.y += 1
        elif self.dir == 'down':
            if self.y > 0 and 0 < self.x < 8:  # 在虚线范围内才能向下移动
                self.y -= 1
        elif self.dir == 'left':
            if self.x > 0 and 0 < self.y < 8:  # 在虚线范围内才能向左移动
                self.x -= 1
        elif self.dir == 'right':
            if self.x < 8 and 0 < self.y < 8:  # 在虚线范围内才能向右移动
                self.x += 1
        elif self.dir == 'stop':
            pass

    def set_position(self, position):
        self.x = position.x
        self.y = position.y
        
    def set_dir(self, dir):
        self.dir = dir
    
    def set_index(self, index):
        self.index = index
    
    def plt_robot(self):
        return plt.Rectangle((self.x + self.index, self.y),
                0.5, 0.5, color='yellow', alpha = 1)
    
    def plt_label(self):
        return plt.text(self.x + self.index, self.y, str(self.item),
                 ha='center', va='center', color = self.color,fontsize=12)
    
    def position_to_index(self,position):
        if self.postion == position:
            return self.index

    def next_position(self):
        if self.dir == 'up':
            return Position.position(self.x, self.y + 1)
        elif self.dir == 'down':
            return Position.position(self.x, self.y - 1)
        elif self.dir == 'left':
            return Position.position(self.x - 1, self.y)
        elif self.dir == 'right':
            return Position.position(self.x + 1, self.y)
    
    def catch_delivery(self, delivery):
        self.item = delivery.item
        delivery.robot = self
        delivery.if_catched()

    def send_delivery(self, delivery):
        delivery.robot = None
        self.item = None
