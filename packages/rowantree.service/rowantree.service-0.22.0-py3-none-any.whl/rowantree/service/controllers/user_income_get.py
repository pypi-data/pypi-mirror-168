""" User Income Get Controller Definition """
from rowantree.contracts import IncomeSourceType, UserIncome
from rowantree.service.sdk import UserIncomeGetResponse

from .abstract_controller import AbstractController


class UserIncomeGetController(AbstractController):
    """
    User Income Get Controller
    Gets (unique) list of user incomes.

    Methods
    -------
    execute(self, user_guid: str) -> UserIncomeGetResponse
        Executes the command.
    """

    def execute(self, user_guid: str) -> UserIncomeGetResponse:
        """
        Gets (unique) list of user incomes.

        Parameters
        ----------
        user_guid: str
            The target user guid.

        Returns
        -------
        user_incomes: UserIncomeGetResponse
            A (unique) list of user incomes.
        """

        income_sources: dict[IncomeSourceType, UserIncome] = self.dao.user_income_get(user_guid=user_guid)
        return UserIncomeGetResponse(incomes=income_sources)
