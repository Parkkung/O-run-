import arcade


class Ora:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self, delta):
        if self.y > 600:
            self.y = 0
        self.y += 5

class World():
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.score = 0

    def update(self,delta):
        pass