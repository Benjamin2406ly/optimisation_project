import matplotlib.pyplot as plt
import Position
import Delivery

class robot:    
    def __init__(self, position:tuple, dir, index, delivery:Delivery.delivery, color):
        # position.x: 0.25,
        # position.y: -0.75,
        # dir: 'up',
        # index: 0   
        # occupied: False
        self.position = Position.position(position[0], position[1])
        self.delivery = delivery
        self.position.robot = self
        self.item = None
        if self.delivery != None: 
            self.delivery.robot = self
            self.item = self.delivery.item
            self.in_task = True
        self.dir = dir
        self.index = index
        self.color = color
        self.edgecolor = ''
    
    def move(self):
        if self.dir == 'up':
            if self.position.y < 16 and -2 < self.position.x < 16:  # 在虚线范围内才能向上移动
                self.position.y += 2
        elif self.dir == 'down':
            if self.position.y > -2 and -2 < self.position.x < 16:  # 在虚线范围内才能向下移动
                self.position.y -= 2
        elif self.dir == 'left':
            if self.position.x > -2 and -2 < self.position.y < 16:  # 在虚线范围内才能向左移动
                self.position.x -= 2
        elif self.dir == 'right':
            if self.position.x < 16 and -2 < self.position.y < 16:  # 在虚线范围内才能向右移动
                self.position.x += 2
        elif self.dir == 'stop':
            pass
        
    def set_dir(self, direction):
        self.dir = direction
    
    def set_index(self, i):
        self.index = i
    
    def plt_robot(self):
        Rectangle_robot=(plt.Rectangle((self.position.x + 0.5, self.position.y + 0.5),
                1, 1, color=self.color, alpha = 1))
        return Rectangle_robot
    
    def plt_label(self):
        Label_robot = [self.position.x + 1, self.position.y + 1, str(self.item)]
        return Label_robot

    def next_position(self):
        if self.dir == 'up':
            return Position.position(self.position.x, self.position.y + 2)
        elif self.dir == 'down':
            return Position.position(self.position.x, self.position.y - 2)
        elif self.dir == 'left':
            return Position.position(self.position.x - 2, self.position.y)
        elif self.dir == 'right':
            return Position.position(self.position.x + 2, self.position.y)
    
    def catch_delivery(self, dlvery:Delivery.delivery):
        self.delivery = dlvery
        self.in_task = True
        self.item = dlvery.item
        self.delivery.robot = self
        self.delivery.if_catched()
        self.edgecolor = 'black'

    def send_delivery(self):
        self.delivery.robot = None
        self.delivery = None
        self.item = None
        self.in_task = False
        self.edgecolor = 'blue'