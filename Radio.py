__author__ = "TheComet"

import pygame
from Updateable import Updateable


class Radio(Updateable):
    def __init__(self, options, pos, set_value):
        self.pos = pos
        self.set_value = set_value
        self.options = options
        self.font = pygame.font.Font("sans.ttf", 18)
        self.pressed_index = 0

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, option in enumerate(self.options):
                if (event.pos[0]-self.pos[0])**2 + (event.pos[1]-self.pos[1]-i*20)**2 < 64:
                    self.pressed_index = i
                    self.set_value(i)
                    break

    def draw(self, surface):
        for i, option in enumerate(self.options):
            text = self.font.render(option, True, (255, 255, 255))
            rect = text.get_rect()
            rect.center = (0, self.pos[1] + i*20)
            rect.left = self.pos[0] + 20
            surface.blit(text, rect)

            self.__draw_button(surface, (self.pos[0], self.pos[1]+i*20), self.pressed_index==i)

    def __draw_button(self, surface, pos, pressed):
        pygame.draw.circle(surface, (255, 255, 255), pos, 8, 1)
        if pressed:
            pygame.draw.circle(surface, (255, 255, 255), pos, 3, 3)
