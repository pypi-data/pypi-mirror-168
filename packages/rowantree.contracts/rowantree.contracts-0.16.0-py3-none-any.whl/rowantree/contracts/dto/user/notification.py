""" User Notification Definition """

from datetime import datetime

from ..base_model import BaseModel
from .event import UserEvent


class UserNotification(BaseModel):
    """
    UserNotification DTO
    Defines a user notification.

    Attributes
    ----------
    index: int
        Event ID (unique)
    timestamp: datetime
        Server time that the event occured.
    event: UserEvent
        An UserEvent object of the event.
    """

    index: int
    timestamp: datetime
    event: UserEvent
