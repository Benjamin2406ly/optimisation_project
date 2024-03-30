import matplotlib.pyplot as plt
import Position
import Robot

class sendwindow:
    def __init__(self, name, position:tuple):
        self.position = Position.position(position[0], position[1])
        self.name = name
        self.highlight = False

    def plt_sendwindow(self):
        Rectangle_sendwindow=(plt.Rectangle((self.position.x, self.position.y),
                2, 2, linewidth = 1, edgecolor = 'white', alpha = 0.5))
        Highlight_sendwindow=(plt.Rectangle((self.position.x, self.position.y),
                2, 2, edgecolor='yellow', facecolor='none', linewidth=3))
        if self.highlight:
            return Highlight_sendwindow
        else:
            return Rectangle_sendwindow

    def plt_label(self):
        Label_sendwindow = [self.position.x+1, self.position.y+1, str(self.name)]
        return Label_sendwindow
    
    # def robot_send_delivery(self, robot:Robot.robot):
    #     if self.position.if_eq(robot.position) and robot.delivery.item == self.name:
    #         robot.send_delivery()
    #         self.highlight = True
    #     else:
    #         self.highlight = False