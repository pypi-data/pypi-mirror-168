from enum import Enum, auto


class Disqualification(Enum):
    CAPSIZE = auto()
    FALL = auto()
    SINKING = auto()
    VIOLATION = auto()
    DISQUALIFICATION_AFTER_START = auto()
    ENGINE_STOP = auto()
    UNFINISHED = auto()
    REPAYMENT_OTHER_THAN_FLYING_AND_LATENESS = auto()
    FLYING = auto()
    LATENESS = auto()
    ABSENT = auto()
