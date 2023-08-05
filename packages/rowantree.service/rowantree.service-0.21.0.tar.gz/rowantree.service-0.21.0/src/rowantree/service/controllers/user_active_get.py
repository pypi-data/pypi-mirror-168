""" User Active Get Controller Definition """

import logging

from starlette import status
from starlette.exceptions import HTTPException

from rowantree.service.sdk import UserActiveGetStatus

from ..services.db.incorrect_row_count_error import IncorrectRowCountError
from .abstract_controller import AbstractController


class UserActiveGetController(AbstractController):
    """
    User Active Get Controller
    Gets the user active state.
    """

    def execute(self, user_guid: str) -> UserActiveGetStatus:
        """
        Gets the user active state.
        If the requested user does not exist we do not expose this in the response. (information leakage).
        If the user is not found or is inactive we return an inactive response.

        Parameters
        ----------
        user_guid: str
            The user guid to look up.

        Returns
        -------
        user_active: UserActiveGetStatus
            The user active state object.
        """

        try:
            active: bool = self.dao.user_active_state_get(user_guid=user_guid)
            return UserActiveGetStatus(active=active)
        except IncorrectRowCountError as error:
            logging.debug("caught: {%s}", str(error))
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unable to find user") from error
