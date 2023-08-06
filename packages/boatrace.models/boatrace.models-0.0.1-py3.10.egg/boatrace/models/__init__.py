from .betting_method import BettingMethod
from .branch import Branch
from .disqualification import Disqualification
from .gender import Gender
from .motor_parts import MotorParts
from .prefecture import Prefecture
from .race_grade import RaceGrade
from .race_kind import RaceKind
from .race_laps import RaceLaps
from .racer_rank import RacerRank
from .stadium_tel_code import StadiumTelCode
from .weather import Weather
from .winning_trick import WinningTrick

VERSION = (0, 0, 1)
__version__ = ".".join([str(x) for x in VERSION])
