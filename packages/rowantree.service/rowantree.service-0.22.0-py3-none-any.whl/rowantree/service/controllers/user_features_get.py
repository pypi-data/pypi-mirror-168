""" User Features Get Controller Definition """
import logging

from starlette import status
from starlette.exceptions import HTTPException

from rowantree.contracts import FeatureType
from rowantree.service.sdk import FeaturesGetResponse

from ..services.db.incorrect_row_count_error import IncorrectRowCountError
from .abstract_controller import AbstractController


class UserFeaturesGetController(AbstractController):
    """
    User Features Get Controller
    Gets the unique list of user features.

    Methods
    -------
    execute(self, user_guid: str) -> UserFeatures
        Executes the command.
    """

    def execute(self, user_guid: str) -> FeaturesGetResponse:
        """
        Gets the unique list of user features.

        Parameters
        ----------
        user_guid: str
            The target user guid.

        Returns
        -------
        user_features: UserFeatures
            A unique list of user features.
        """

        try:
            features: set[FeatureType] = self.dao.user_features_get(user_guid=user_guid)
            return FeaturesGetResponse(features=features)
        except IncorrectRowCountError as error:
            # User did not exist (received an empty tuple)
            logging.debug("caught: {%s}", str(error))
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unable to find user") from error
