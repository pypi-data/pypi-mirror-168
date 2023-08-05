""" User Income Set Controller Definition """

from rowantree.service.sdk import UserIncomeSetRequest

from ..controllers.abstract_controller import AbstractController


class UserIncomeSetController(AbstractController):
    """
    User Income Set Controller
    Sets a user income. (Creates or dismisses a number of workers of the type).

    Methods
    -------
    execute(self, user_guid: str, request: UserIncomeSetRequest) -> None
        Executes the command.
    """

    def execute(self, user_guid: str, request: UserIncomeSetRequest) -> None:
        """
        Sets a user income. (Creates or dismisses a number of workers of the type).

        Parameters
        ----------
        user_guid: str
            The target user guid.
        request: UserIncomeSetRequest
            The UserIncomeSetRequest object for the update.
        """

        self.dao.user_income_set(user_guid=user_guid, transaction=request)
