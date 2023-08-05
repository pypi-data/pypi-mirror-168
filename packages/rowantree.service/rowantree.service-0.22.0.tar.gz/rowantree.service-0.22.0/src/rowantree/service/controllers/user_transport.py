""" User Transport Controller Definition """
import logging

from starlette import status
from starlette.exceptions import HTTPException

from rowantree.contracts import UserFeatureState
from rowantree.service.sdk import UserTransportRequest

from ..contracts.sql_exception_error import SqlExceptionError
from ..services.db.incorrect_row_count_error import IncorrectRowCountError
from .abstract_controller import AbstractController


class UserTransportController(AbstractController):
    """
    User Transport Controller
    Performs a user transport. (feature to feature change)

    Methods
    -------
    execute(self, user_guid: str, request: UserTransportRequest) -> UserFeatureState
        Executes the command.
    """

    def execute(self, user_guid: str, request: UserTransportRequest) -> UserFeatureState:
        """
        Performs a user transport. (feature to feature change)

        Parameters
        ----------
        user_guid: str
            The target user guid.
        request: UserTransportRequest
            The UserTransportRequest to perform.

        Returns
        -------
        active_feature_state: UserFeatureState
            The user's new active feature state.
        """

        try:
            return self.dao.user_transport(user_guid=user_guid, location=request.location)
        except IncorrectRowCountError as error:
            logging.debug("caught: {%s}", str(error))
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unable to find user") from error
        except SqlExceptionError as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable move to location") from error
