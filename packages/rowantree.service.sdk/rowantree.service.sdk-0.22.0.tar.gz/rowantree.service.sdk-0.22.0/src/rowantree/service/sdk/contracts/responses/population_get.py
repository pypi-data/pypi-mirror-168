""" PopulationGetResponse Definition """

from rowantree.contracts import BaseModel


class PopulationGetResponse(BaseModel):
    """
    PopulationGetResponse DTO
    Defines a user population.

    Attributes
    ----------
    population: int
        The current size of the user population.
    """

    population: int
