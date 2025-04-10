import math
from random import random

import arcade

from obstacles import Obstacles
from torpedo import Torpedo

from centipede import Centipede


class CentipideKiller(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.shooter_xpos = 500
        self.shooter_ypos = 100
        self.shooter_radius = 30
        self.shooter_xdir = 1
        self.shooter_ydir = 1
        self.torpedoList = []
        self.obstacleList = []
        self.torpedoRadius = 15
        self.obstacleRadius = 15
        for i in range(50):
            self.obstacleList.append(
                Obstacles(random() * (self.width - 300) + 200, random() * (self.height - 100) + 200))
        self.centipede = Centipede(self.height, self.width)
        self.points = 0
        self.gameover = False

    def on_draw(self):
        if self.gameover:
            arcade.draw_text('GAMEOVER - points: ' + str(self.points), 300, 300, font_size=30)
        else:
            self.clear(arcade.color.BLACK)
            arcade.draw_circle_filled(self.shooter_xpos, self.shooter_ypos, self.shooter_radius, arcade.color.GHOST_WHITE)

            self.shooter_xpos += 2 * self.shooter_xdir

            if self.shooter_xpos >= self.width or self.shooter_xpos <= 0:
                self.shooter_xdir *= -1

            if len(self.torpedoList) > 0:
                for Torpedo in self.torpedoList:
                    Torpedo.update()
                    arcade.draw_circle_filled(Torpedo.torpedo_xpos, Torpedo.torpedo_ypos, 15, arcade.color.RED)
                if self.torpedoList[0].torpedo_ypos > self.height:
                    self.torpedoList.pop(0)

            for i in range(len(self.obstacleList)):
                arcade.draw_circle_filled(self.obstacleList[i].obstacle_xpos, self.obstacleList[i].obstacle_ypos, 10,
                                          arcade.color.GOLD)

            if len(self.torpedoList) > 0:
                for Torpedo in self.torpedoList:
                    hitTorpedo = False
                    for obstacles in self.obstacleList:
                        if math.dist((Torpedo.torpedo_xpos, Torpedo.torpedo_ypos),
                                     (obstacles.obstacle_xpos, obstacles.obstacle_ypos)) <= (
                                self.torpedoRadius + self.obstacleRadius):
                            hitTorpedo = True
                            self.obstacleList.remove(obstacles)
                            self.points += 1
                    if hitTorpedo:
                        self.torpedoList.remove(Torpedo)

            if len(self.centipede.centipedeList) > 0:

                for segment in self.centipede.centipedeList:
                    arcade.draw_circle_filled(segment.seg_xpos, segment.seg_ypos, segment.radius, arcade.color.PURPLE)
                    segment.update()
                    if segment.seg_xpos < 0 or segment.seg_xpos > self.width:
                        segment.moveDownAndReverse()
                    for obstacles in self.obstacleList:
                        if math.dist((segment.seg_xpos, segment.seg_ypos),
                                     (obstacles.obstacle_xpos, obstacles.obstacle_ypos)) <= (
                                segment.radius + self.obstacleRadius):
                            segment.moveDownAndReverse()
                    for torpedo in self.torpedoList:
                        if math.dist((segment.seg_xpos, segment.seg_ypos),
                                     (torpedo.torpedo_xpos, torpedo.torpedo_ypos)) <= (
                                segment.radius + self.torpedoRadius):
                            self.centipede.centipedeList.remove(segment)
                            self.torpedoList.remove(torpedo)
                            self.obstacleList.append(Obstacles(segment.seg_xpos, segment.seg_ypos))
                            self.points += 1
                    if math.dist((segment.seg_xpos, segment.seg_ypos), (self.shooter_xpos, self.shooter_ypos)) <= (segment.radius + self.shooter_radius):
                        self.gameover = True
                    if len(self.centipede.centipedeList) == 0:
                        self.gameover = True
            arcade.draw_text('points: ' + str(self.points), 100, 30, font_size=15)



    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LEFT:
            self.shooter_xdir = -1
        elif symbol == arcade.key.RIGHT:
            self.shooter_xdir = 1
        elif symbol == arcade.key.SPACE:
            if len(self.torpedoList) <= 10:
                self.torpedoList.append(Torpedo(self.shooter_xpos, self.shooter_ypos))


if __name__ == '__main__':
    arcade.window = CentipideKiller(1000, 600, 'blahblah')
    arcade.run()
