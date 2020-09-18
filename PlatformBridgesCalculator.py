__author__ = "TheComet"


UAIR_HITSTUN = 29

JUMPSQUAT = 3
UAIR_DURATION = 26
UAIR_AC = 18
LANDING_LAG = 2
SLOW_LANDING_LAG = 14


class EndOfJumpData(Exception):
    pass


class PlatformBridgesCalculator:
    def __init__(self):
        self.jump1 = 0
        self.dj1 = 0
        self.uair1 = 0
        self.uair1_end = 0
        self.uair2 = 0
        self.uair2_end = 0
        self.uair2_ac_start = 0
        self.land = 0

        self.sh2 = 0
        self.uair3 = 0
        self.uair3_end = 0

        # hitx is first frame where uair connects
        # hitx_end is the first frame when the opponent becomes actionable
        self.hit1 = 0
        self.hit1_end = 0
        self.hit2 = 0
        self.hit2_end = 0
        self.hit3 = 0
        self.hit3_end = 0

        # Variables tweakable by the player
        self.jump1_delay = 0
        self.dj1_delay = 0
        self.uair1_delay = 0
        self.uair2_delay = 0
        self.sh2_delay = 0
        self.plat_height = 0.5

        self.do_fullhop = False

    def calculate_frames(self):
        ################################################################
        # Pikachu frame calculations
        ################################################################

        # Start at frame 1
        self.jump1 = 1 + self.jump1_delay

        # Assume we're doing an IDJ
        self.dj1 = self.jump1 + JUMPSQUAT + self.dj1_delay

        # uair is on same frame as double jump, or later
        self.uair1 = self.dj1 + self.uair1_delay
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

        # Calculate where frame 18 of uair2 begins (AC start)
        self.uair2_ac_start = self.uair2 + UAIR_AC - 1

        # Figure out when pikachu lands
        self.land = self.find_landing_frame(self.uair2)

        # Calculate next short hop
        if self.land - self.uair2 < UAIR_AC - 1:
            self.sh2 = self.land + SLOW_LANDING_LAG + self.sh2_delay
        else:
            self.sh2 = self.land + LANDING_LAG + self.sh2_delay

        # Exact same code as above, but for uair3 and uair4
        self.uair3 = self.sh2 + JUMPSQUAT

        # Don't have enough sh data for the full uair3, so cap it
        self.uair3_end = self.sh2 + JUMPSQUAT + len(SH_DATA)

        self.hit3 = self.uair3 + 7 - 1
        self.hit3_end = self.hit3 + UAIR_HITSTUN

    def get_height_at_frame_before_landing_on_platform(self, frame):
        if frame < self.dj1:
            idx = frame - self.jump1 - JUMPSQUAT
            if self.do_fullhop:
                return FH_DATA[idx] if idx >= 0 else 0
            else:
                return SH_DATA[idx] if idx >= 0 else 0

        # figure out how many jump1 frames we use and calculate offset it causes from ground
        jump1_frames = self.dj1 - self.jump1 - JUMPSQUAT
        if jump1_frames > 0:
            if self.do_fullhop:
                height = FH_DATA[jump1_frames - 1]
            else:
                height = SH_DATA[jump1_frames - 1]
        else:
            height = 0

        # Look up height in double jump data and add to offset from previous fullhop/shorthop
        idx = frame - self.dj1
        if idx >= len(DJ_DATA):
            raise EndOfJumpData()
        height += DJ_DATA[idx]

        # Detect landing on platform. Use uair2 frame to determine when we start descending. Should be close enough
        if frame > self.uair2:
            height = max(height, self.plat_height)

        return height

    def get_height_at_frame_after_platfom(self, frame):
        if frame < self.sh2 + JUMPSQUAT:
            return self.plat_height

        idx = frame - self.sh2 - JUMPSQUAT
        return SH_DATA[idx] + self.plat_height

    def get_height_at_frame(self, frame):
        if frame < self.land:
            return self.get_height_at_frame_before_landing_on_platform(frame)
        return self.get_height_at_frame_after_platfom(frame)

    def find_landing_frame(self, uair2):
        land_on = uair2 + 1
        try:
            while self.get_height_at_frame_before_landing_on_platform(land_on) > self.plat_height:
                land_on += 1
        except EndOfJumpData:
            pass
        return land_on


GRAVITY = 0.095
FALL_SPEED = 1.55
FAST_FALL_SPEED = 2.48

SH_DATA = [
    0.25,
    0.425,
    0.55,
    0.7,
    0.85,
    0.95,
    1.075,
    1.175,
    1.25,
    1.325
]

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

DJ_DATA = [
    0.15,
    0.35,
    0.55,
    0.85,
    1.05,
    1.275,
    1.5,
    1.7,
    1.925,
    2.125,
    2.3,
    2.5,
    2.7,
    2.85,
    3,
    3.15,
    3.25,
    3.3,
    3.35,
    3.4,
    3.45,
    3.5,
    3.5,
    3.525,
    3.525,
    3.55,
    3.55,
    3.55,
    3.55,
    3.525,
    3.525,
    3.5,
    3.5,
    3.475,
    3.425,
    3.375,
    3.3,
    3.225,
    3.175,
    3.075,
    2.975,
    2.85,
    2.7,
    2.55,
    2.4,
    2.3,
    2.175,
    2.025,
    1.85,
    1.7,
    1.5,
    1.375,
    1.25,
    1.1,
    0.95,
    0.8,
    0.65,
    0.55,
    0.4,
    0.25
]

if __name__ == '__main__':
    c = PlatformBridgesCalculator()
    h = c.get_height_at_frame(4)