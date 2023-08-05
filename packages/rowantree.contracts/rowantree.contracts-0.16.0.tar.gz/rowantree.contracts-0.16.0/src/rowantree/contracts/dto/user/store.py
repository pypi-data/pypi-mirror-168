""" UserStore Definition """

from typing import Optional

from ...types.store_type import StoreType
from ..base_model import BaseModel


class UserStore(BaseModel):
    """
    UserStore DTO
    Defines a user store.

    Attributes
    ----------
    name: StoreType
        The StoreType of the store.
    description: Optional[str]
        The optional description of the store.
    amount: int
        The amount of the user store.
    """

    name: StoreType
    description: Optional[str]
    amount: int
