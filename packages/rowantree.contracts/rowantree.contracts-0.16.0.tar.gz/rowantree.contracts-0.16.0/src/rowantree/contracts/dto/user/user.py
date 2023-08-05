""" User Definition """

from typing import Optional

from ..base_model import BaseModel
from .state import UserState


class User(BaseModel):
    """
    User DTO
    Defines a User

    Attributes
    ----------
    guid: str
        The GUID of the user.
    state: Optional[UserState]
        The optional user state.
    """

    guid: str
    state: Optional[UserState]
