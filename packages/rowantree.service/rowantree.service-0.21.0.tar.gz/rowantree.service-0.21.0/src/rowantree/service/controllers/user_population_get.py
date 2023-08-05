""" User Population Get Controller Definition """
import logging

from starlette import status
from starlette.exceptions import HTTPException

from rowantree.service.sdk import PopulationGetResponse

from ..services.db.incorrect_row_count_error import IncorrectRowCountError
from .abstract_controller import AbstractController


class UserPopulationGetController(AbstractController):
    """
    User Population Get Controller
    Gets the user population.

    Methods
    -------
    execute(self, user_guid: str) -> UserPopulation
        Executes the command.
    """

    def execute(self, user_guid: str) -> PopulationGetResponse:
        """
        Gets the user population.

        Parameters
        ----------
        user_guid: str
            The target user guid.

        Returns
        -------
        user_population: UserPopulation
            User population object.
        """

        try:
            population: int = self.dao.user_population_by_guid_get(user_guid=user_guid)
            return PopulationGetResponse(population=population)
        except IncorrectRowCountError as error:
            logging.debug("caught: {%s}", str(error))
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unable to find user") from error
