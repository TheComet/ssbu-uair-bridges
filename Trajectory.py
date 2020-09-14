__author__ = "TheComet"


import Config
import pygame
from Updateable import Updateable


def points_to_segments(points):
    for i in range(len(points) - 1):
        yield points[i], points[i+1]


class Trajectory(Updateable):
    def __init__(self, calc):
        self.calc = calc

    def draw(self, surface):
        points = list(self.points())
        for i, seg in enumerate(points_to_segments(points)):
            if self.calc.uair1 <= i < self.calc.uair1_end:
                pygame.draw.line(surface, Config.UAIR1_COLOR, seg[0], seg[1], 1)
            elif self.calc.uair2 <= i < self.calc.uair2_end:
                pygame.draw.line(surface, Config.UAIR2_COLOR, seg[0], seg[1], 1)
            else:
                pygame.draw.line(surface, Config.TRAJECTORY_COLOR, seg[0], seg[1], 1)

        for i, point in enumerate(points):
            if self.calc.uair1 <= i <= self.calc.uair1_end:
                pygame.draw.circle(surface, Config.UAIR1_COLOR, point, 2, 1)
            elif self.calc.uair2 <= i <= self.calc.uair2_end:
                pygame.draw.circle(surface, Config.UAIR2_COLOR, point, 2, 1)
            else:
                pygame.draw.circle(surface, Config.TRAJECTORY_COLOR, point, 2, 1)

            if i == self.calc.hit1 or i == self.calc.hit2:
                pygame.draw.circle(surface, Config.HIT_COLOR, point, 4, 1)
            elif i == self.calc.ff1:
                pygame.draw.circle(surface, Config.FF_COLOR, point, 4, 1)

    def points(self):
        for i in range(self.calc.land1):
            yield int(i * Config.SCALEX + Config.OFFSETX),\
                  int(self.calc.get_height_at_frame(self.calc.ff1, i) * Config.SCALEY + Config.OFFSETY)
