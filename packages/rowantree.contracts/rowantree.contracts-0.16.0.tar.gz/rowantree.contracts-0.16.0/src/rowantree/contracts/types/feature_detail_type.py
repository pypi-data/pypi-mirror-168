""" User Feature State Definition """
from enum import Enum


class FeatureDetailType(str, Enum):
    """User Feature State Enumeration"""

    SHADOWY_GROVE = "A Shadowy Grove"
    ROWAN_TREE_LIT_BY_FIRELIGHT = "A Rowan Tree Lit By Firelight"
    SILENT_FOREST = "A Silent Forest"
    LONELY_HUT = "A Lonely Hut"
    COZY_HELMET = "A Cozy Hamlet"
    QUAINT_VILLAGE = "A Quaint Village"
    BUSTLING_TOWN = "A Bustling Town"
    SWARMING_CITY = "A Swarming City"
