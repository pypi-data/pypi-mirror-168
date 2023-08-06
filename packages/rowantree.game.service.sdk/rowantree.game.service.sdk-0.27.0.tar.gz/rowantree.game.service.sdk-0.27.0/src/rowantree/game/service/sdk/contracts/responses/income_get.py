""" UserIncomeGetResponse Definition """

from rowantree.contracts import BaseModel, IncomeSourceType, UserIncome


class UserIncomeGetResponse(BaseModel):
    """
    UserIncomeGetResponse DTO
    A dictionary of user incomes, keyed by income name.
    """

    incomes: dict[IncomeSourceType, UserIncome]
