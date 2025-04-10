import arcade


class CentipedeSegment:
    def __init__(self, seg_xpos, seg_ypos, radius, direction):
        self.seg_xpos = seg_xpos
        self.seg_ypos = seg_ypos
        self.radius = radius
        self.direction = direction

    def update(self):
        self.seg_xpos += self.direction * 5

    def moveDownAndReverse(self):
        self.seg_ypos -= self.radius
        self.direction *= -1
        self.seg_xpos += 10 * self.direction
