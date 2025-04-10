import arcade

from centipedeSegment import CentipedeSegment


class Centipede:
    def __init__(self, screenHeight, screenWidth):
        self.screenHeight = screenHeight
        self.screenWidth = screenWidth
        self.centipedeList = []
        for i in range(1, 11):
            self.centipedeList.append(CentipedeSegment(i * 15, screenHeight-15, 10, 1))


