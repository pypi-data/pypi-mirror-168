""" Abstract Controller Definition """

from abc import abstractmethod
from typing import Any, Optional

from rowantree.contracts import BaseModel

from ..services.db.dao import DBDAO


class AbstractController(BaseModel):
    """
    Abstract Controller

    Attributes
    ----------
    dao: DBDAO
        The database DAO.
    """

    dao: DBDAO

    @abstractmethod
    def execute(self, *args, **kwargs) -> Optional[Any]:
        """Should be implemented in the subclass"""
