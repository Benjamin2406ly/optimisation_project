import matplotlib.pyplot as plt
import Position

class initwindow(Position):
    def _int_(self, index, position, delivery):
        super()._int_(position[0], position[1])
        self.index = index
        self.delivery = delivery

    def plt_initwindow(self):
        return plt.Rectangle((self.position.x, self.position.y),
                1, 1, color='blue', alpha = 0.5)
    
    def plt_label(self):
        return plt.text(self.position.x, self.position.y - 1, str(self.index + 1),
                 ha='center', va='center', color = 'red',fontsize=12)
    
    def robot_catch_delivery(self, robot, delivery):
        if robot.position == self.position:
            robot.catch_delivery(delivery)

    def set_delivery(self, delivery):
        self.delivery = delivery
