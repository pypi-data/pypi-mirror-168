""" User Feature Type Definition """
from enum import Enum


class FeatureType(str, Enum):
    """User Feature Type Enumeration"""

    ROOM = "room"
    OUTSIDE = "outside"
    WORLD = "world"
    SPACESHIP = "spaceship"
