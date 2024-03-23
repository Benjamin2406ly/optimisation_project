class delivery:
    def __init__(self, item):
        self.item = item
        self.robot = None

    def if_catched(self):
        if self.robot == None:
            return False
        else:
            return True