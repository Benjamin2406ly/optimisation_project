import matplotlib.pyplot as plt
import Position

class initwindow:
    def __init__(self, index, position, delivery):
        self.position = Position.position(position[0], position[1])
        self.index = index
        self.delivery = delivery

    def plt_initwindow(self,ax):
        ax.add_patch(plt.Rectangle((self.position.x, self.position.y),
                1, 1, linewidth=1, edgecolor='white'))
    
    def plt_label(self,ax):
        ax.text(self.position.x + 0.5, self.position.y - 0.5, str(self.index),
                ha='center', va='center', color = 'red',fontsize=12)
    
    def robot_catch_delivery(self, robot, delivery):
        if self.position.if_eq(robot.position) and self.delivery != None:
            robot.catch_delivery(delivery)
            self.delivery = None

    def set_delivery(self, delivery):
        self.delivery = delivery
