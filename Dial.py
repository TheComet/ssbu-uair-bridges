__author__ = "TheComet"

import pygame
from Updateable import Updateable


class Dial(Updateable):
    def __init__(self, text, pos, dial_offset, minmax, set_value):
        self.text = text
        self.pos = pos
        self.dial_offset = dial_offset
        self.minmax = minmax
        self.set_value = set_value
        self.value = 0

        self.font = pygame.font.Font('sans.ttf', 18)

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (event.pos[0]-self.pos[0]-self.dial_offset-20)**2 + (event.pos[1]-self.pos[1])**2 < 50 and self.value < self.minmax[1]:
                self.value += 1
                self.set_value(self.value)
            if (event.pos[0] - self.pos[0]-self.dial_offset+20)**2 + (event.pos[1]-self.pos[1])**2 < 50 and self.value > self.minmax[0]:
                self.value -= 1
                self.set_value(self.value)

    def draw(self, surface):
        self.__draw_triangle(surface, (self.pos[0]+self.dial_offset+20, self.pos[1]),  1)
        self.__draw_triangle(surface, (self.pos[0]+self.dial_offset-20, self.pos[1]), -1)

        text = self.font.render(f'{self.value}', True, (255, 255, 255))
        rect = text.get_rect()
        rect.center = (self.pos[0] + self.dial_offset, self.pos[1])
        surface.blit(text, rect)

        text = self.font.render(self.text, True, (255, 255, 255))
        rect = text.get_rect()
        rect.center = self.pos
        rect.left = self.pos[0]
        surface.blit(text, rect)

    def __draw_triangle(self, surface, pos, scalex):
        pygame.draw.line(surface, (255, 255, 255), (pos[0], pos[1]+7), (pos[0], pos[1]-7), 1)
        pygame.draw.line(surface, (255, 255, 255), (pos[0], pos[1]-7), (pos[0]+7*scalex, pos[1]), 1)
        pygame.draw.line(surface, (255, 255, 255), (pos[0]+7*scalex, pos[1]), (pos[0], pos[1]+7), 1)
