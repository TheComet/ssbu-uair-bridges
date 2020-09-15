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
                color = Config.UAIR1_COLOR
            elif self.calc.uair2 <= i < self.calc.land1:
                color = Config.UAIR2_COLOR
            elif self.calc.uair3 <= i < self.calc.uair3_end:
                color = Config.UAIR1_COLOR
            elif self.calc.uair4 <= i < self.calc.land2:
                color = Config.UAIR2_COLOR
            elif self.calc.uair5 <= i < self.calc.uair5_end:
                color = Config.UAIR1_COLOR
            else:
                color = Config.TRAJECTORY_COLOR

            pygame.draw.line(surface, color, seg[0], seg[1], 1)

        for i, point in enumerate(points):
            if self.calc.uair1 <= i <= self.calc.uair1_end:
                color = Config.UAIR1_COLOR
            elif self.calc.uair2 <= i <= self.calc.land1:
                color = Config.UAIR2_COLOR
            elif self.calc.uair3 <= i <= self.calc.uair3_end:
                color = Config.UAIR1_COLOR
            elif self.calc.uair4 <= i <= self.calc.land2:
                color = Config.UAIR2_COLOR
            elif self.calc.uair5 <= i <= self.calc.uair5_end:
                color = Config.UAIR1_COLOR
            else:
                color = Config.TRAJECTORY_COLOR

            pygame.draw.circle(surface, color, point, 2, 1)

            if i in (self.calc.hit1, self.calc.hit2, self.calc.hit3, self.calc.hit4, self.calc.hit5):
                pygame.draw.circle(surface, Config.HIT_COLOR, point, 4, 1)
            if i in (self.calc.ff1, self.calc.ff2):
                pygame.draw.circle(surface, Config.FF_COLOR, point, 6, 1)
            if i == self.calc.uair2_ac_start or i == self.calc.uair4_ac_start:
                pygame.draw.circle(surface, Config.AC_START_COLOR, point, 4, 1)

    def points(self):
        # first full hop
        for i in range(self.calc.uair5_end):
            yield int(i * Config.SCALEX + Config.OFFSETX),\
                  int(self.calc.get_height_at_frame(i) * Config.SCALEY + Config.OFFSETY)
