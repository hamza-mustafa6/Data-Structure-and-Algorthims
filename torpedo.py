import arcade

class Torpedo:
    def __init__(self, torpedo_xpos, torpedo_ypos):
        self.torpedo_xpos = torpedo_xpos
        self.torpedo_ypos = torpedo_ypos


    def update(self):
        self.torpedo_ypos += 10