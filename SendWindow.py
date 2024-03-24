import matplotlib.pyplot as plt
import Position
import Robot

class sendwindow:
    def __init__(self, name, position):
        self.position = Position.position(position[0], position[1])
        self.name = name

    def plt_sendwindow(self,ax):
        ax.add_patch(plt.Rectangle((self.position.x, self.position.y),
                2, 2, linewidth = 1, edgecolor = 'white', alpha = 0.5))
    
    def plt_label(self,ax):
        ax.text(self.position.x+1, self.position.y+1, str(self.name),
                ha='center', va='center', color = 'red',fontsize=12)
    
    def highlight(self,ax):
        ax.add_patch(plt.Rectangle((self.position.x, self.position.y),
                2, 2, edgecolor='yellow', facecolor='none', linewidth=3))
    
    def robot_send_delivery(self, robot:Robot.robot, ax):
        if self.position.if_eq(robot.position) and robot.delivery.item == self.name:
            robot.send_delivery()
            self.highlight(ax)