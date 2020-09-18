__author__ = "TheComet"

import pygame
from Updateable import Updateable
from FullBridgeTrajectory import FullBridgeTrajectory
from FullBridgesCalculator import FullBridgesCalculator
from FullBridgeHitstun import FullBridgeHitstun
from PlatformBridgesTrajectory import PlatformBridgesTrajectory
from PlatformBridgesCalculator import PlatformBridgesCalculator
from PlatformBridgesHitstun import PlatformBridgesHitstun
from Dial import Dial
from Radio import Radio
from Checkbox import Checkbox
from time import time


def full_bridge_updateables():
    global sync_reps
    sync_reps = False

    def assign_fh1(value):
        calc.fh1_delay = value
        if sync_reps:
            calc.fh2_delay = value
            calc.fh3_delay = value
            fh2_delay.value = value
            fh3_delay.value = value
        calc.calculate_frames()

    def assign_uair1(value):
        calc.uair1_delay = value
        if sync_reps:
            calc.uair3_delay = value
            calc.uair5_delay = value
            uair3_delay.value = value
            uair5_delay.value = value
        calc.calculate_frames()

    def assign_uair2(value):
        calc.uair2_delay = value
        if sync_reps:
            calc.uair4_delay = value
            uair4_delay.value = value
        calc.calculate_frames()

    def assign_ff1(value):
        calc.ff1_delay = value
        if sync_reps:
            calc.ff2_delay = value
            ff2_delay.value = value
        calc.calculate_frames()

    def assign_fh2(value):
        calc.fh2_delay = value
        if sync_reps:
            calc.fh1_delay = value
            calc.fh3_delay = value
            fh1_delay.value = value
            fh3_delay.value = value
        calc.calculate_frames()

    def assign_uair3(value):
        calc.uair3_delay = value
        if sync_reps:
            calc.uair1_delay = value
            calc.uair5_delay = value
            uair1_delay.value = value
            uair5_delay.value = value
        calc.calculate_frames()

    def assign_uair4(value):
        calc.uair4_delay = value
        if sync_reps:
            calc.uair2_delay = value
            uair2_delay.value = value
        calc.calculate_frames()

    def assign_ff2(value):
        calc.ff2_delay = value
        if sync_reps:
            calc.ff1_delay = value
            ff1_delay.value = value
        calc.calculate_frames()

    def assign_fh3(value):
        calc.fh3_delay = value
        if sync_reps:
            calc.fh1_delay = value
            calc.fh2_delay = value
            fh1_delay.value = value
            fh2_delay.value = value
        calc.calculate_frames()

    def assign_uair5(value):
        calc.uair5_delay = value
        if sync_reps:
            calc.uair1_delay = value
            calc.uair3_delay = value
            uair1_delay.value = value
            uair3_delay.value = value
        calc.calculate_frames()

    def assign_ff_mode(enable):
        calc.pin_ff_to_uair = enable
        ff1_delay.minmax[0] = -10 if enable else 0
        ff1_delay.value = max(ff1_delay.value, 0)
        ff2_delay.minmax[0] = -10 if enable else 0
        ff2_delay.value = max(ff2_delay.value, 0)
        calc.calculate_frames()

    def assign_sync_reps(enable):
        global sync_reps
        sync_reps = enable

    uair1_delay = Dial("uair1 delay", (10, 10), [-1, 10], assign_uair1)
    uair2_delay = Dial("uair2 delay", (10, 30), [0, 10], assign_uair2)
    uair3_delay = Dial("uair3 delay", (10, 50), [-1, 10], assign_uair3)
    uair4_delay = Dial("uair4 delay", (10, 70), [0, 10], assign_uair4)
    uair5_delay = Dial("uair5 delay", (10, 90), [-1, 10], assign_uair5)
    fh1_delay = Dial("fh1 delay", (10, 120), [0, 10], assign_fh1)
    fh2_delay = Dial("fh2 delay", (10, 140), [0, 10], assign_fh2)
    fh3_delay = Dial("fh3 delay", (10, 160), [0, 10], assign_fh3)
    ff1_delay = Dial("ff1 delay", (10, 190), [0, 10], assign_ff1)
    ff2_delay = Dial("ff2 delay", (10, 210), [0, 10], assign_ff2)

    calc = FullBridgesCalculator()
    calc.calculate_frames()

    return [
        FullBridgeTrajectory(calc),
        FullBridgeHitstun(calc),
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
        Radio(("Calculate optimal fastfall", "Pin fastfall to uair"), (200, 10), assign_ff_mode),
        Checkbox("Synchronize repititions", (200, 60), assign_sync_reps, False)
    ]


def platform_bridges_updatedables():

    # platform heights
    platform_heights = [
        1.9906,  # lylat
        2.4119,  # BF
        2.4119,  # SBF
        2.7075,  # PS2
        2.6982,  # Yoshi's
        2.7518,  # Town
        2.8698,  # Smashville
        3,       # Kalos
    ]

    def assign_jump1(value):
        calc.jump1_delay = value
        calc.calculate_frames()

    def assign_dj1(value):
        calc.dj1_delay = value
        calc.calculate_frames()

    def assign_uair1(value):
        calc.uair1_delay = value
        calc.calculate_frames()

    def assign_uair2(value):
        calc.uair2_delay = value
        calc.calculate_frames()

    def assign_sh2(value):
        calc.sh2_delay = value
        calc.calculate_frames()

    def assign_fh(enable):
        calc.do_fullhop = enable
        calc.calculate_frames()

    def assign_plat_height(value):
        calc.plat_height = platform_heights[value]
        calc.calculate_frames()

    calc = PlatformBridgesCalculator()
    calc.plat_height = platform_heights[0]
    calc.calculate_frames()

    return [
        PlatformBridgesTrajectory(calc),
        PlatformBridgesHitstun(calc),
        Dial("jump1 delay", (10, 10), (0, 10), assign_jump1),
        Dial("dj delay",    (10, 30), (0, 10), assign_dj1),
        Dial("uair1 delay", (10, 50), (0, 10), assign_uair1),
        Dial("uair2 delay", (10, 70), (0, 10), assign_uair2),
        Dial("sh2 delay",   (10, 90), (0, 10), assign_sh2),
        Checkbox("Do fullhop", (50, 120), assign_fh, False),
        Radio(("Lylat", "BF", "SBF", "PS2", "Yoshi's", "Town", "Smashville", "Kalos"), (255, 10), assign_plat_height)
    ]


class Window(Updateable):
    def __init__(self, width, height):
        self.dimensions = width, height
        self.screen = pygame.display.set_mode(self.dimensions)

        def change_scenario(idx):
            if idx == 0:
                self.__updateables = base_updatedables + full_bridge_scenario
            elif idx == 1:
                self.__updateables = base_updatedables + platform_bridges_scenario

        base_updatedables = [
            self,
            Dial("Scenario", (width - 150, 10), (0, 1), change_scenario)
        ]

        full_bridge_scenario = full_bridge_updateables()
        platform_bridges_scenario = platform_bridges_updatedables()

        change_scenario(0)

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
