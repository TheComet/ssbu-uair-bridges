__author__ = "TheComet"

import pygame
from Updateable import Updateable


class Checkbox(Updateable):
    def __init__(self, text, pos, set_value, enabled=False):
        self.text = text
        self.pos = pos
        self.set_value = set_value
        self.enabled = enabled

        self.font = pygame.font.Font("sans.ttf", 18)

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (event.pos[0] - self.pos[0])**2 + (event.pos[1] - self.pos[1])**2 < 64:
                self.enabled = not self.enabled
                self.set_value(self.enabled)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(self.pos[0] - 6, self.pos[1] - 6, 12, 12), 1)

        text = self.font.render(self.text, True, (255, 255, 255))
        rect = text.get_rect()
        rect.center = self.pos
        rect.left = self.pos[0] + 20
        surface.blit(text, rect)

        if self.enabled:
            pygame.draw.line(surface, (255, 255, 255), self.pos, (self.pos[0] - 4, self.pos[1] - 4), 1)
            pygame.draw.line(surface, (255, 255, 255), self.pos, (self.pos[0] + 8, self.pos[1] - 8), 1)
