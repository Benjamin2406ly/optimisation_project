class position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.occupied = False
        self.robot = None

    def set_x(self, x):
        self.x = x
    
    def set_y(self, y):
        self.y = y

    def determine_occupied(self):
        if self.robot == None:
            self.occupied = False
        else:
            self.occupied = True