class position:
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y
        self.robot = None

    def set_x(self, x):
        self.x = x
    
    def set_y(self, y):
        self.y = y
    
    def if_eq(self, other):
        if other is not None:
            return self.x == other.x and self.y == other.y
        else:
            return False