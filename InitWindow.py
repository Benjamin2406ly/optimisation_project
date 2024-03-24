import matplotlib.pyplot as plt
import Position
import Delivery
import Robot

class initwindow:
    def __init__(self, index, position, delivery):
        self.position = Position.position(position[0], position[1])
        self.index = index
        self.delivery = Delivery.delivery(delivery)

    def plt_initwindow(self,ax):
        ax.add_patch(plt.Rectangle((self.position.x, self.position.y),
                2, 2, linewidth=1, edgecolor='white'))
    
    def plt_label(self,ax):
        ax.text(self.position.x + 1, self.position.y - 1, str(self.index)+':'+str(self.delivery.item),
                ha='center', va='center', color = 'green',fontsize=8)
    
    def robot_catch_delivery(self, robot:Robot.robot):
        if self.position.if_eq(robot.position) and self.delivery != None:
            robot.catch_delivery(self.delivery)
            self.delivery = None

    def set_delivery(self, dlvery:Delivery.delivery):
        self.delivery = dlvery
