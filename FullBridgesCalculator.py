__author__ = "TheComet"


UAIR_HITSTUN = 29

JUMPSQUAT = 3
UAIR_DURATION = 26
UAIR_AC = 18
FF_LANDING_LAG = 4
SLOW_LANDING_LAG = 14


class FullBridgesCalculator:
    def __init__(self):
        self.fh1 = 0
        self.uair1 = 0
        self.uair1_end = 0
        self.uair2 = 0
        self.uair2_end = 0
        self.uair2_ac_start = 0
        self.ff1 = 0
        self.land1 = 0

        self.fh2 = 0
        self.uair3 = 0
        self.uair3_end = 0
        self.uair4 = 0
        self.uair4_end = 0
        self.uair4_ac_start = 0
        self.ff2 = 0
        self.land2 = 0

        self.fh3 = 0
        self.uair5 = 0
        self.uair5_end = 0

        # hitx is first frame where uair connects
        # hitx_end is the first frame when the opponent becomes actionable
        self.hit1 = 0
        self.hit1_end = 0
        self.hit2 = 0
        self.hit2_end = 0
        self.hit3 = 0
        self.hit3_end = 0
        self.hit4 = 0
        self.hit4_end = 0
        self.hit5 = 0
        self.hit5_end = 0

        # Variables tweakable by the player
        self.fh1_delay = 0
        self.uair1_delay = 0
        self.uair2_delay = 0
        self.ff1_delay = 0
        self.fh2_delay = 0
        self.uair3_delay = 0
        self.uair4_delay = 0
        self.ff2_delay = 0
        self.fh3_delay = 0
        self.uair5_delay = 0

        # fastfall calculation mode. If true, the fastfall timing will be relative to the second uair. If false, the
        # fastfall timing is calculated so pikachu lands on frame 18 of uair2.
        self.pin_ff_to_uair = False

    def delay_uair1(self, frames):
        self.uair1_delay = frames
        self.calculate_frames()

    def calculate_frames(self):
        ################################################################
        # Pikachu frame calculations
        ################################################################

        # Start at frame 1
        self.fh1 = 1 + self.fh1_delay

        # Earliest possible input for a fh uair is 4 frames after jump was pressed
        self.uair1 = self.fh1 + JUMPSQUAT + 1 + self.uair1_delay
        self.uair1_end = self.uair1 + UAIR_DURATION - 1

        # First active uair hitbox is frame 4. There are 3 strong hitboxes, 2 weak. Tests show it usually connects
        # 7 frames after input
        self.hit1 = self.uair1 + 7 - 1
        self.hit1_end = self.hit1 + UAIR_HITSTUN

        # Pretty much same calculations for uair2
        self.uair2 = self.uair1_end + 1 + self.uair2_delay
        self.uair2_end = self.uair2 + UAIR_DURATION - 1

        self.hit2 = self.uair2 + 7 - 1
        self.hit2_end = self.hit2 + UAIR_HITSTUN

        # Find optimal fast fall timing and find landing frame
        if self.pin_ff_to_uair:
            self.ff1 = self.hit2 + 1 + self.ff1_delay
        else:
            self.ff1 = self.find_optimal_ff_frame(self.uair2) + self.ff1_delay
        self.land1 = self.find_landing_frame(self.uair2, self.ff1)

        # Calculate where frame 18 of uair2 begins (AC start)
        self.uair2_ac_start = self.uair2 + UAIR_AC - 1

        # Calculate next full hop
        if self.land1 - self.uair2 < UAIR_AC - 1:
            self.fh2 = self.land1 + SLOW_LANDING_LAG + self.fh2_delay
        else:
            self.fh2 = self.land1 + FF_LANDING_LAG + self.fh2_delay

        # Exact same code as above, but for uair3 and uair4
        self.uair3 = self.fh2 + JUMPSQUAT + 1 + self.uair3_delay
        self.uair3_end = self.uair3 + UAIR_DURATION - 1

        self.hit3 = self.uair3 + 7 - 1
        self.hit3_end = self.hit3 + UAIR_HITSTUN

        self.uair4 = self.uair3_end + 1 + self.uair4_delay
        self.uair4_end = self.uair4 + UAIR_DURATION - 1

        self.hit4 = self.uair4 + 7 - 1
        self.hit4_end = self.hit4 + UAIR_HITSTUN

        if self.pin_ff_to_uair:
            self.ff2 = self.hit4 + 1 + self.ff2_delay
        else:
            self.ff2 = self.find_optimal_ff_frame(self.uair4) + self.ff2_delay
        self.land2 = self.find_landing_frame(self.uair4, self.ff2)
        self.uair4_ac_start = self.uair4 + UAIR_AC - 1

        if self.land2 - self.uair4 < UAIR_AC - 1:
            self.fh3 = self.land2 + SLOW_LANDING_LAG + self.fh3_delay
        else:
            self.fh3 = self.land2 + FF_LANDING_LAG + self.fh3_delay

        self.uair5 = self.fh3 + JUMPSQUAT + 1 + self.uair5_delay
        self.uair5_end = self.uair5 + UAIR_DURATION - 1

        self.hit5 = self.uair5 + 7 - 1
        self.hit5_end = self.hit5 + UAIR_HITSTUN

    def get_height_at_frame_with_ff(self, frame, ff):
        if frame < self.fh1 + 3:
            return 0

        if frame - self.fh1 - 3 < len(FH_DATA):
            if frame <= ff:
                return FH_DATA[frame - self.fh1 - 3]
            return FH_DATA[ff - self.fh1 - 3] + (ff - frame) * FAST_FALL_SPEED * GRAVITY

        # land, delay and jumpsquat
        if frame < self.fh2 + 3:
            return 0

        if frame - self.fh2 - 3 < len(FH_DATA):
            if frame <= ff:
                return FH_DATA[frame - self.fh2 - 3]
            height = FH_DATA[ff - self.fh2 - 3] + (ff - frame) * FAST_FALL_SPEED * GRAVITY
            return height if height > 0 else 0

        # land, delay and jumpsquat
        if frame < self.fh3 + 3:
            return 0

        return FH_DATA[frame - self.fh3 - 3]

    def get_height_at_frame(self, frame):
        if frame < self.fh1 + 3:
            return 0

        if frame - self.fh1 - 3 < len(FH_DATA):
            if frame <= self.ff1:
                return FH_DATA[frame - self.fh1 - 3]
            height = FH_DATA[self.ff1 - self.fh1 - 3] + (self.ff1 - frame) * FAST_FALL_SPEED * GRAVITY
            if height > 0:
                return height

        # land, delay and jumpsquat
        if frame < self.fh2 + 3:
            return 0

        if frame - self.fh2 - 3 < len(FH_DATA):
            if frame <= self.ff2:
                return FH_DATA[frame - self.fh2 - 3]
            height = FH_DATA[self.ff2 - self.fh2 - 3] + (self.ff2 - frame) * FAST_FALL_SPEED * GRAVITY
            if height > 0:
                return height

        # land, delay and jumpsquat
        if frame < self.fh3 + 3:
            return 0

        return FH_DATA[frame - self.fh3 - 3]

    def find_landing_frame(self, uair2, ff):
        land_on = uair2 + 1
        while self.get_height_at_frame_with_ff(land_on, ff) > 0:
            land_on += 1
        return land_on

    def find_optimal_ff_frame(self, uair2):
        # just brute force it
        ff = uair2
        while self.find_landing_frame(uair2, ff) - uair2 > UAIR_AC - 1:
            ff -= 1
        while self.find_landing_frame(uair2, ff) - uair2 < UAIR_AC - 1:
            ff += 1

        return ff


GRAVITY = 0.095
FALL_SPEED = 1.55
FAST_FALL_SPEED = 2.48

FH_DATA = [
    0.75,   # first airborne frame
    1.25,
    1.65,
    1.95,
    2.1,
    2.25,
    2.4,
    2.5,
    2.625,
    2.725,
    2.85,
    2.95,
    3.02,
    3.1,
    3.15,
    3.19,
    3.24,
    3.29,
    3.34,
    3.37,
    3.415,
    3.46,
    3.49,
    3.5,
    3.5,
    3.475,
    3.45,
    3.4,
    3.33,
    3.25,
    3.175,
    3.075,
    2.975,
    2.875,
    2.8,
    2.7,
    2.575,
    2.45,  # linear fall speed starts here approximately (frame 38)
    2.3,
    2.15,
    2.04,
    1.9,
    1.75,
    1.6,
    1.45,
    1.3,
    1.15,
    1,
    0.85,
    0.7,
    0.55,
    0.4,
    0.25,
    0
]

if __name__ == '__main__':
    c = FullBridgesCalculator()
    print(f"uair1: {c.uair1}")
    print(f"uair2: {c.uair2}")
    print(f"ff: {c.ff1}")
    print(f"land: {c.land1}")
