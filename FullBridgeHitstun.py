__author__ = "TheComet"

from Updateable import Updateable
import Config
import pygame

DTHROW_ADVANTAGE = 18


class FullBridgeHitstun(Updateable):
    def __init__(self, calc):
        self.calc = calc

        self.font = pygame.font.Font("sans.ttf", 18)
        self.text = self.font.render("Hitstun", True, (255, 255, 255))

    def draw(self, surface):
        # Draw horizontal line
        start = (Config.OFFSETX1, Config.OFFSETY1 + 100)
        end = (Config.OFFSETX1 + self.calc.uair5_end * Config.SCALEX1, Config.OFFSETY1 + 100)
        pygame.draw.line(surface, Config.TRAJECTORY_COLOR, start, end, 1)

        # "hitstun" text
        rect = self.text.get_rect()
        rect.left = Config.OFFSETX1
        rect.bottom = Config.OFFSETY1 + 100
        surface.blit(self.text, rect)

        self.draw_hit(surface, 0, DTHROW_ADVANTAGE, self.calc.hit1)
        self.draw_hit(surface, self.calc.hit1, self.calc.hit1_end, self.calc.hit2)
        self.draw_hit(surface, self.calc.hit2, self.calc.hit2_end, self.calc.hit3)
        self.draw_hit(surface, self.calc.hit3, self.calc.hit3_end, self.calc.hit4)
        self.draw_hit(surface, self.calc.hit4, self.calc.hit4_end, self.calc.hit5)

    def draw_hit(self, surface, hit_start, hit_end, next_hit_start):
        if next_hit_start < hit_end:
            color = (100, 255, 100)
        elif next_hit_start > hit_end:
            color = (255, 100, 100)
        else:
            color = (255, 255, 100)

        hit = hit_end if hit_end < next_hit_start else next_hit_start
        start = (hit_start * Config.SCALEX1 + Config.OFFSETX1, Config.OFFSETY1 + 100)
        end = (hit * Config.SCALEX1 + Config.OFFSETX1, Config.OFFSETY1 + 100)
        pygame.draw.line(surface, color, start, end, 1)

        start = (end[0], self.calc.get_height_at_frame(hit) * Config.SCALEY1 + Config.OFFSETY1 - 10)
        end = (end[0], end[1] + 10)
        pygame.draw.line(surface, Config.TRAJECTORY_COLOR, start, end, 1)
        text = self.font.render(f"{next_hit_start - hit_end}", True, color)
        rect = text.get_rect()
        rect.top = Config.OFFSETY1 + 100 + 2
        rect.left = hit * Config.SCALEX1 + Config.OFFSETX1 + 5
        surface.blit(text, rect)
