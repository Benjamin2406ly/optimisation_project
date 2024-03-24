class position:
    def __init__(self, x:int, y:int):
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
    
    def if_eq(self, other):
        return self.x == other.x and self.y == other.y