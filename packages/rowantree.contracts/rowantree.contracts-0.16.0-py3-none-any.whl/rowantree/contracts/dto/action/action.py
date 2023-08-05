""" Command Queue Action Definition """
from ..base_model import BaseModel


class Action(BaseModel):
    """
    Action DTO
    This DTO defines the command queue action.

    Attributes
    ----------
    name: str
        The name of the command (stored prodecure name)
    arguments: list
        The arguments to pass to the command.
    """

    name: str
    arguments: list
