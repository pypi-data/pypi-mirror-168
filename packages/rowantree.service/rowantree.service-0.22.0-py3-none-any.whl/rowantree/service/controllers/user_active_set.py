""" User Active Set Controller Definition """

from rowantree.service.sdk import UserActiveGetStatus

from .abstract_controller import AbstractController


class UserActiveSetController(AbstractController):
    """
    User Active Set Controller
    Sets the user active state.

    Methods
    -------
    execute(self, user_guid: str, request: UserActive) -> UserActive
        Executes the command.
    """

    def execute(self, user_guid: str, request: UserActiveGetStatus) -> None:
        """
        Sets the user active state.

        Parameters
        ----------
        user_guid: str
            The user guid to target.
        request: UserActiveGetStatus
            The active state to set the user to.
        """

        # This is atomic and idempotent.  If it failed then we most likely are running into
        # either database level connectivity, config, or table leve locks...
        # TODO: the underlying calls need to provide more context on status of this call.

        self.dao.user_active_state_set(user_guid=user_guid, active=request.active)
