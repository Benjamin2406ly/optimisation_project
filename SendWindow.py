import matplotlib.pyplot as plt
import Position

class sendwindow:
    def __init__(self, name, position):
        self.position = Position.position(position[0], position[1])
        self.name = name

    def plt_sendwindow(self,ax):
        ax.add_patch(plt.Rectangle((self.position.x, self.position.y),
                1, 1, linewidth = 1, edgecolor = 'white', alpha = 0.5))
    
    def plt_label(self,ax):
        ax.text(self.position.x+0.5, self.position.y+0.5, str(self.name),
                ha='center', va='center', color = 'red',fontsize=12)
    
    def highlight(self,ax):
        ax.add_patch(plt.Rectangle((self.position.x, self.position.y),
                1, 1, edgecolor='yellow', facecolor='none', linewidth=2))
    
    def robot_send_delivery(self, robot, delivery, ax):
        if self.position.if_eq(robot.position) and delivery.item == self.name:
            robot.send_delivery(delivery)
            self.highlight(ax)
            del(delivery)
