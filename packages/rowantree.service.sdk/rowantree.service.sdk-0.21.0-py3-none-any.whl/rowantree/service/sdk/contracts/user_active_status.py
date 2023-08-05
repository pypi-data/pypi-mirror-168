""" User Active Definition """
from rowantree.contracts import BaseModel


class UserActiveGetStatus(BaseModel):
    """
    UserActiveGetStatus DTO
    Defines the user active state.

    Attributes
    ----------
    active: bool
        The user active state.
    """

    user_guid: str
    active: bool
