""" User Transport Request Definition """
from rowantree.contracts import BaseModel, FeatureType


class UserTransportRequest(BaseModel):
    """
    User Transport Request DTO

    NOTE/TODO:
        We've mixed location and feature.  We need to refactor location -> feature.

    Attributes
    ----------
    location: FeatureType
        The name of the feature (location).
    """

    user_guid: str
    location: FeatureType
