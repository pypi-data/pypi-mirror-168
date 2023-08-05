""" User Create Controller Definition """


from starlette import status
from starlette.exceptions import HTTPException

from rowantree.contracts import User

from ..services.db.incorrect_row_count_error import IncorrectRowCountError
from .abstract_controller import AbstractController


class UserCreateController(AbstractController):
    """
    User Create Controller
    Creates a user.

    Methods
    -------
    execute(self) -> User
        Executes the command.
    """

    def execute(self, request: str) -> User:
        """
        Creates a user.

        Returns
        -------
        user: User
            The newly created user.
        """

        try:
            return self.dao.user_create_by_guid(user_guid=request)
        except IncorrectRowCountError as error:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Unable to create new user") from error
