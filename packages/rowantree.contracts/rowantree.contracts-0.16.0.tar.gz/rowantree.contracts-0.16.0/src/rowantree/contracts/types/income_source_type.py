" Income Source Type Definition "
from enum import Enum


class IncomeSourceType(str, Enum):
    """Income Source Type Enumeration"""

    GATHERER = "gatherer"
    HUNTER = "hunter"
    TRAPPER = "trapper"
    FARMER = "farmer"
    TANNER = "tanner"
    CHARCUTIER = "charcutier"
    IRON_MINER = "iron miner"
    COAL_MINER = "coal miner"
    SULPHUR_MINE = "sulphur miner"
    STEELWORKER = "steelworker"
    ARMOURER = "armourer"
