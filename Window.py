__author__ = "TheComet"

import pygame
from Updateable import Updateable
from Trajectory import Trajectory
from UairBridgesCalculator import UairBridgesCalculator
from Dial import Dial
from Hitstun import Hitstun
from Radio import Radio
from time import time


class Window(Updateable):
    def __init__(self, width, height):
        self.dimensions = width, height
        self.screen = pygame.display.set_mode(self.dimensions)
        self.calc = UairBridgesCalculator()

        def assign_fh1(value):
            self.calc.fh1_delay = value
            self.calc.calculate_frames()
        def assign_uair1(value):
            self.calc.uair1_delay = value
            self.calc.calculate_frames()
        def assign_uair2(value):
            self.calc.uair2_delay = value
            self.calc.calculate_frames()
        def assign_ff1(value):
            self.calc.ff1_delay = value
            self.calc.calculate_frames()
        def assign_fh2(value):
            self.calc.fh2_delay = value
            self.calc.calculate_frames()
        def assign_uair3(value):
            self.calc.uair3_delay = value
            self.calc.calculate_frames()
        def assign_uair4(value):
            self.calc.uair4_delay = value
            self.calc.calculate_frames()
        def assign_ff2(value):
            self.calc.ff2_delay = value
            self.calc.calculate_frames()
        def assign_fh3(value):
            self.calc.fh3_delay = value
            self.calc.calculate_frames()
        def assign_uair5(value):
            self.calc.uair5_delay = value
            self.calc.calculate_frames()
        def assign_ff_mode(enable):
            self.calc.pin_ff_to_uair = enable
            ff1_delay.minmax[0] = -10 if enable else 0
            ff1_delay.value = max(ff1_delay.value, 0)
            ff2_delay.minmax[0] = -10 if enable else 0
            ff2_delay.value = max(ff2_delay.value, 0)
            self.calc.calculate_frames()

        uair1_delay = Dial("uair1 delay", (10, 10),  [0, 10], assign_uair1)
        uair2_delay = Dial("uair2 delay", (10, 30),  [0, 10], assign_uair2)
        uair3_delay = Dial("uair3 delay", (10, 50),  [0, 10], assign_uair3)
        uair4_delay = Dial("uair4 delay", (10, 70),  [0, 10], assign_uair4)
        uair5_delay = Dial("uair5 delay", (10, 90),  [0, 10], assign_uair5)
        fh1_delay   = Dial("fh1 delay",   (10, 110), [0, 10], assign_fh1)
        fh2_delay   = Dial("fh2 delay",   (10, 130), [0, 10], assign_fh2)
        fh3_delay   = Dial("fh3 delay",   (10, 150), [0, 10], assign_fh3)
        ff1_delay   = Dial("ff1 delay",   (10, 170), [0, 10], assign_ff1)
        ff2_delay   = Dial("ff2 delay",   (10, 190), [0, 10], assign_ff2)

        self.__updateables = [
            self,
            Trajectory(self.calc),
            Hitstun(self.calc),
            uair1_delay,
            uair2_delay,
            uair3_delay,
            uair4_delay,
            uair5_delay,
            fh1_delay,
            fh2_delay,
            fh3_delay,
            ff1_delay,
            ff2_delay,
            Radio(("Calculate optimal fastfall", "Pin fastfall to uair"), (200, 10), assign_ff_mode)
        ]

        self.__last_time_updated = None
        self.__running = False

    def enter_main_loop(self):
        self.__last_time_updated = time()
        self.__running = True
        while self.__running:
            self.__process_events()
            self.__update()
            self.__draw()

    def __process_events(self):
        for event in pygame.event.get():
            for updatedable in self.__updateables:
                if updatedable.process_event(event):
                    break

    def __update(self):
        dt = self.__update_timestep()
        for updateable in self.__updateables:
            updateable.update(dt)

    def __update_timestep(self):
        new_time = time()
        dt = new_time - self.__last_time_updated
        self.__last_time_updated = new_time
        return dt

    def __draw(self):
        self.screen.fill((0, 0, 0))

        for updateable in self.__updateables:
            updateable.draw(self.screen)

        pygame.display.flip()

    def process_event(self, event):
        if event.type == pygame.QUIT:
            self.__running = False
