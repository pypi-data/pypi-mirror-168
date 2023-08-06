""" MerchantTransformsGetResponse Definition """

from rowantree.contracts import BaseModel, StoreType


class MerchantTransformsGetResponse(BaseModel):
    """
    MerchantTransformsGetResponse DTO
    The (unique) set of user merchants.
    """

    merchants: set[StoreType]
