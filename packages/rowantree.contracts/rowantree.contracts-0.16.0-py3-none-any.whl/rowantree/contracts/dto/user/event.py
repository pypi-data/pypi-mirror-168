""" User Event Definition """

from typing import Union

from ...types.store_type import StoreType
from ...types.user_event_other_type import UserEventOtherType
from ..base_model import BaseModel


class UserEvent(BaseModel):
    """
    UserEvent DTO
    Defines an event of a user.
    In practice this is a state change for the user as a result of an in-world story or encounter.

    Attributes
    ----------
    title: str
        The title of the event.
    text: dict[int, str]
        A numbered set of entries meant to be rendered sequentially user-side.
    reward: dict[Union[UserEventOtherType, StoreType], int]
        Dictionary of rewards (positive deltas to apply to the user)
    curse: dict[Union[UserEventTypeOther, StoreType], int]
        Dictionary of curses (negative deltas to apply to the user)
    requirements: dict[Union[UserEventOtherType, StoreType], int]
        Dictionary of requirements (amounts user must meet to trigger the event)
    """

    title: str
    text: dict[int, str]
    notification: dict[int, str]
    reward: dict[Union[UserEventOtherType, StoreType], int]
    curse: dict[Union[UserEventOtherType, StoreType], int]
    requirements: dict[Union[UserEventOtherType, StoreType], int]
