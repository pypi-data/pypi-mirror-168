""" Merchant Transform Request Definition """
from rowantree.contracts import BaseModel, StoreType


class MerchantTransformRequest(BaseModel):
    """
    Merchant Transform Request DTO

    Attributes
    ----------
    store_name: StoreType
        The name of the store to transform.
    """

    store_name: StoreType
