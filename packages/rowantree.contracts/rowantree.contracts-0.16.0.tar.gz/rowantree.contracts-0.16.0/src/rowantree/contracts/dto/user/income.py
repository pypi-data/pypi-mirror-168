""" User Income Definition """

from typing import Optional

from ...types.income_source_type import IncomeSourceType
from ..base_model import BaseModel


class UserIncome(BaseModel):
    """
    User Income DTO

    Attributes
    ----------
    amount: int
        The number of this income type
    name: IncomeSourceType
        The income type
    description: Optional[str]
        The optional description of the income
    """

    amount: int
    name: IncomeSourceType
    description: Optional[str]
