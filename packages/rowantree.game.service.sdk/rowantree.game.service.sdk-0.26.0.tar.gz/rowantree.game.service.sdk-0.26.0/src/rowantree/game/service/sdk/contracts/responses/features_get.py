""" FeaturesGetResponse Definition """
from rowantree.contracts import BaseModel, FeatureType


class FeaturesGetResponse(BaseModel):
    """
    FeaturesGetResponse DTO
    Defines a list of known user features (locations) of the game world.

    Attributes
    ----------
    features: set[FeatureType]
        A set of user feature types.
    """

    features: set[FeatureType]
