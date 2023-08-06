from enum import IntEnum


class RaceLaps(IntEnum):
    TWO = 2
    THREE = 3


class RaceLapsFactory:
    METRE_PER_A_LAP = 600

    @classmethod
    def create(cls, metre: int):
        return RaceLaps(metre / cls.METRE_PER_A_LAP)
