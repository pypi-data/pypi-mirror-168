""" User Income Set Request Definition """
from rowantree.contracts import BaseModel, IncomeSourceType


class UserIncomeSetRequest(BaseModel):
    """
    User Income Set Request DTO.

    Attributes
    ----------
    income_source_name: IncomeSourceType
        The income source name (worker type)
    amount: int
        The amount to set for the specified type. (As an absolute)
    """

    income_source_name: IncomeSourceType
    amount: int
