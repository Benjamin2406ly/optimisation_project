import matplotlib.pyplot as plt
import Position
import Delivery

class robot:    
    def __init__(self, position, dir, index, delivery, color):
        # position.x: 0.25,
        # position.y: -0.75,
        # dir: 'up',
        # index: 0   
        # occupied: False
        self.position = Position.position(position[0], position[1])
        self.delivery = Delivery.delivery(delivery)
        self.position.robot = self 
        self.delivery.robot = self
        self.dir = dir
        self.index = index
        self.item = self.delivery.item
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
        
    def set_dir(self, direction):
        self.dir = direction
    
    def set_index(self, i):
        self.index = i
    
    def plt_robot(self,ax):
        ax.add_patch(plt.Rectangle((self.position.x + 0.5, self.position.y + 0.5),
                1, 1, color=self.color, alpha = 1))
    
    def plt_label(self,ax):
        ax.text(self.position.x + 1, self.position.y + 1, str(self.item),
                ha='center', va='center', color = 'black',fontsize=8)

    def next_position(self):
        if self.dir == 'up':
            return Position.position(self.position.x, self.position.y + 1)
        elif self.dir == 'down':
            return Position.position(self.position.x, self.position.y - 1)
        elif self.dir == 'left':
            return Position.position(self.position.x - 1, self.position.y)
        elif self.dir == 'right':
            return Position.position(self.position.x + 1, self.position.y)
    
    def catch_delivery(self, dlvery:Delivery.delivery):
        self.delivery = dlvery
        self.in_task = True
        self.delivery.robot = self
        self.delivery.if_catched()

    def send_delivery(self):
        self.delivery.robot = None
        self.delivery = None
        self.item = None
        self.in_task = False
