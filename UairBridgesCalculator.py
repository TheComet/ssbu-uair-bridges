__author__ = "TheComet"


DTHROW_HITSTUN = 18
UAIR_HITSTUN = 27

JUMPSQUAT = 3
UAIR_DURATION = 26
UAIR_AC = 18
AC_LANDING_LAG = 4


class UairBridgesCalculator:
    def __init__(self):
        self.fh1 = 1   # first full hop is fixed to frame 1 always
        self.uair1 = 0
        self.uair1_end = 0
        self.hit1 = 0
        self.uair2 = 0
        self.uair2_end = 0
        self.hit2 = 0
        self.ff1 = 0
        self.land1 = 0

        self.fh2 = 0
        self.uair3 = 0
        self.uair3_end = 0
        self.hit3 = 0
        self.uair4 = 0
        self.uair4_end = 0
        self.hit4 = 0
        self.ff2 = 0
        self.land2 = 0

        # Variables tweakable by the player
        self.uair1_delay = 0
        self.uair2_delay = 0
        self.fh2_delay = 0
        self.uair3_delay = 0
        self.uair4_delay = 0

        self.calculate_frames()

    def delay_uair1(self, frames):
        self.uair1_delay = frames
        self.calculate_frames()

    def calculate_frames(self):
        # Earliest possible input for a fh uair is 4 frames after jump was pressed
        self.uair1 = self.fh1 + JUMPSQUAT + 1 + self.uair1_delay
        self.uair1_end = self.uair1 + UAIR_DURATION - 1

        # First active uair hitbox is frame 4. There are 3 strong hitboxes, 2 weak. Tests show it usually connects 7
        # 7 frames after input
        self.hit1 = self.uair1 + 7 - 1

        self.uair2 = self.uair1_end + 1 + self.uair2_delay
        self.uair2_end = self.uair2 + UAIR_DURATION - 1
        self.hit2 = self.uair2 + 7 - 1

        self.ff1, self.land1 = self.calc_optimal_ff_frame(self.ff1, self.uair2)

    def get_height_at_frame(self, ff, frame):
        if frame <= ff:
            return FH_DATA[frame]
        return FH_DATA[ff] + (ff - frame) * FAST_FALL_SPEED * GRAVITY

    def find_landing_frame(self, ff, uair2):
        land_on = uair2 + 1
        while self.get_height_at_frame(ff, land_on) > 0:
            land_on += 1
        return land_on

    def calc_optimal_ff_frame(self, ff, uair2):
        # just brute force it
        while self.find_landing_frame(ff, uair2) - uair2 > UAIR_AC - 1:
            ff -= 1
        while self.find_landing_frame(ff, uair2) - uair2 < UAIR_AC - 1:
            ff += 1

        return ff, self.find_landing_frame(ff, uair2)


GRAVITY = 0.095
FALL_SPEED = 1.55
FAST_FALL_SPEED = 2.48

FH_DATA = [
    0,
    0,      # frame 1
    0,      # frame 2
    0,      # frame 3
    0.75,   # airborne
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
    2.45,  # linear fall speed starts here approximately (frame 41)
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
    c = UairBridgesCalculator()
    print(f"uair1: {c.uair1}")
    print(f"uair2: {c.uair2}")
    print(f"ff: {c.ff1}")
    print(f"land: {c.land1}")
