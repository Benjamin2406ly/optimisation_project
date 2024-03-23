import matplotlib.pyplot as plt
import Position

class sendwindow(Position.position):
    def __init__(self, name, position):
        super().__init__(position[0], position[1])
        self.index = name

    def plt_sendwindow(self):
        return plt.Rectangle((self.x, self.y),
                1, 1, color='green', alpha = 0.5)
    
    def plt_label(self):
        return plt.text(self.x, self.y, str(self.name),
                 ha='center', va='center', color = 'red',fontsize=12)
    
    def highlight(self):
        return plt.Rectangle((self.x, self.y), 1, 1, edgecolor='yellow', facecolor='none', linewidth=2)
    
    def robot_send_delivery(self, robot, delivery):
        if robot.position == self.position:
            robot.send_delivery(delivery)
            self.highlight()
