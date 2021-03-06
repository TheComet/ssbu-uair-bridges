__author__ = "TheComet"


import Config
import pygame
from Updateable import Updateable


def points_to_segments(points):
    for i in range(len(points) - 1):
        yield points[i], points[i+1]


class DJUairTrajectory(Updateable):
    def __init__(self, calc):
        self.calc = calc
        self.font = pygame.font.Font("sans.ttf", 18)

    def draw(self, surface):
        points = list(self.points())
        for i, seg in enumerate(points_to_segments(points)):
            if self.calc.uair1 <= i < self.calc.uair1_end:
                color = Config.UAIR1_COLOR
            elif self.calc.uair2 <= i < self.calc.uair2_end:
                color = Config.UAIR1_COLOR
            elif self.calc.uair3 <= i < self.calc.land:
                color = Config.UAIR2_COLOR
            elif self.calc.uair4 <= i < self.calc.uair4_end:
                color = Config.UAIR1_COLOR
            else:
                color = Config.TRAJECTORY_COLOR

            pygame.draw.line(surface, color, seg[0], seg[1], 1)

        for i, point in enumerate(points):
            if self.calc.uair1 <= i <= self.calc.uair1_end:
                color = Config.UAIR1_COLOR
            elif self.calc.uair2 <= i <= self.calc.uair2_end:
                color = Config.UAIR1_COLOR
            elif self.calc.uair3 <= i <= self.calc.land:
                color = Config.UAIR2_COLOR
            elif self.calc.uair4 <= i <= self.calc.uair4_end:
                color = Config.UAIR1_COLOR
            else:
                color = Config.TRAJECTORY_COLOR

            pygame.draw.circle(surface, color, point, 2, 1)

            if i in (self.calc.hit1, self.calc.hit2, self.calc.hit3, self.calc.hit4):
                pygame.draw.circle(surface, Config.HIT_COLOR, point, 4, 1)
            if i  == self.calc.ff1:
                pygame.draw.circle(surface, Config.FF_COLOR, point, 6, 1)

            if i == self.calc.uair3_ac_start:
                if self.calc.land - self.calc.uair3 > 17:
                    color = (255, 255, 0)
                elif self.calc.land - self.calc.uair3 < 17:
                    color = (255, 0, 0)
                    self.draw_point_label(surface, "Missed AC", (255, 0, 0), point, (point[0]+15, point[1]+40))
                else:
                    color = (0, 255, 0)
                pygame.draw.circle(surface, color, point, 4, 1)

    def points(self):
        for i in range(self.calc.uair4_end):
            yield int(i * Config.SCALEX3 + Config.OFFSETX3),\
                  int(self.calc.get_height_at_frame(i) * Config.SCALEY3 + Config.OFFSETY3)

    def draw_point_label(self, surface, text, color, target_pos, text_pos):
        text = self.font.render(text, True, color)
        rect = text.get_rect()

        pygame.draw.line(surface, color, target_pos, (text_pos[0], text_pos[1] - 2), 1)
        pygame.draw.line(surface, color, (text_pos[0], text_pos[1] - 2), (text_pos[0]+rect.width, text_pos[1] - 2), 1)

        rect.left = text_pos[0]
        rect.bottom = text_pos[1]
        surface.blit(text, rect)
