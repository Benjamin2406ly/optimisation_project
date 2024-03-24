import Position
class delivery:
    def __init__(self, imformation):
        self.item = imformation[0]
        self.robot = None
        self.sendwindow_position = Position.position(imformation[1][0], imformation[1][1])

    def if_catched(self):
        if self.robot == None:
            return False
        else:
            return True