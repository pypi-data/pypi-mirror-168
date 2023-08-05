""" Database DAO Definition """

import logging
import socket
from datetime import datetime
from typing import Optional, Tuple

import mysql.connector
from mysql.connector import IntegrityError, errorcode
from mysql.connector.pooling import MySQLConnectionPool, PooledMySQLConnection
from starlette import status
from starlette.exceptions import HTTPException

from rowantree.contracts import (
    ActionQueue,
    BaseModel,
    FeatureDetailType,
    FeatureType,
    IncomeSourceType,
    StoreType,
    User,
    UserEvent,
    UserFeatureState,
    UserIncome,
    UserNotification,
    UserStore,
)
from rowantree.service.sdk import UserIncomeSetRequest

from ...contracts.duplicate_key_error import DuplicateKeyError
from ...contracts.sql_exception_error import SqlExceptionError
from .incorrect_row_count_error import IncorrectRowCountError


class DBDAO(BaseModel):
    """
    Database DAO

    Attributes
    ----------
    cnxpool: MySQLConnectionPool
        MySQL Connection Pool
    """

    cnxpool: MySQLConnectionPool

    def merchant_transform_perform(self, user_guid: str, store_name: str) -> None:
        """
        Perform a merchant transform.

        Parameters
        ----------
        user_guid: str
            The target user guid.
        store_name: str
            The name of the store to perform the transform on.
        """

        args: list = [user_guid, store_name]
        self._call_proc("peformMerchantTransformByGUID", args)

    def user_active_feature_get(self, user_guid: str) -> FeatureType:
        """
        Gets user's active feature/location.

        Parameters
        ----------
        user_guid: str
            The target user guid.

        Returns
        -------
        user_feature: FeatureType
            The active user feature.
        """

        args: list = [
            user_guid,
        ]
        rows: list[Tuple[str]] = self._call_proc("getUserActiveFeatureByGUID", args)
        if len(rows) != 1:
            # User did not exist (received an empty tuple)
            message: str = f"Result count was not exactly one. Received: {rows}"
            logging.debug(message)
            raise IncorrectRowCountError(message)
        return FeatureType(rows[0][0])

    def user_active_feature_state_details_get(self, user_guid: str) -> UserFeatureState:
        """
        Get User Active Feature/Location Including Details.

        Parameters
        ----------
        user_guid: str
            The target user guid.

        Returns
        -------
        user_feature: UserFeatureState
            The active user feature/location with details.
        """

        args: list = [
            user_guid,
        ]
        rows: list[Tuple[str, Optional[str]]] = self._call_proc("getUserActiveFeatureStateDetailsByGUID", args)
        if len(rows) != 1:
            # User did not exist (received an empty tuple)
            message: str = f"Result count was not exactly one. Received: {rows}"
            logging.debug(message)
            raise IncorrectRowCountError(message)

        return UserFeatureState(details=FeatureDetailType(rows[0][0]), description=rows[0][1])

    def users_active_get(self) -> set[str]:
        """
        Get Active Users.

        Returns
        -------
        active_user_guids: set[str]
            A (unique) set of user guids which are active.
        """

        active_user_guids: set[str] = set()
        rows: list[Tuple] = self._call_proc("getActiveUsers", [])
        for response_tuple in rows:
            active_user_guids.add(response_tuple[0])
        return active_user_guids

    def user_active_state_get(self, user_guid: str) -> bool:
        """
        Get user active state.

        Parameters
        ----------
        user_guid: str
        The target user guid.

        Returns
        -------
        user_active: UserActive
            The user active state.
        """

        args: list[str, int] = [
            user_guid,
        ]
        rows: list[Tuple[int]] = self._call_proc("getUserActivityStateByGUID", args)
        if len(rows) != 1:
            raise IncorrectRowCountError(f"Result count was not exactly one. Received: {rows}")
        if rows[0][0] == 1:
            return True
        return False

    def user_active_state_set(self, user_guid: str, active: bool) -> None:
        """
        Set user's active state.
        # TODO: the underlying calls need to provide more context on status of this call.

        Parameters
        ----------
        user_guid: str
            The target user guid.
        active: bool
            The active state to set.
        """

        args: list = [
            user_guid,
        ]
        if active:
            proc = "setUserActiveByGUID"
        else:
            proc = "setUserInactiveByGUID"
        self._call_proc(name=proc, args=args)

    def user_create_by_guid(self, user_guid: str) -> User:
        """
        Create a user.
        TODO this returns nothing, needs more detail from the db.

        Returns
        -------
        user: User
            The created user.
        """

        args = [user_guid]
        try:
            self._call_proc("createUserByGUID", args)
        except (IntegrityError, DuplicateKeyError) as error:
            message: str = f"User already exists: {user_guid}, {str(error)}"
            logging.debug(message)
            raise IncorrectRowCountError(message) from error
        return User(guid=user_guid)

    def user_delete(self, user_guid: str) -> None:
        """
        Delete user.
        TODO: the underlying calls need to provide more context on status of this call.

        Parameters
        ----------
        user_guid: str
            The target user guid.
        """

        args: list = [
            user_guid,
        ]
        self._call_proc("deleteUserByGUID", args)

    def user_features_get(self, user_guid: str) -> set[FeatureType]:
        """
        Get user features.

        Parameters
        ----------
        user_guid: str
            The target user guid.

        Returns
        -------
        user_features: UserFeatures
            User features object.
        """

        features: set[FeatureType] = set()

        args: list = [
            user_guid,
        ]
        rows: list[Tuple[str]] = self._call_proc("getUserFeaturesByGUID", args)

        if rows is None or len(rows) == 0:
            # User does not exist ot had no features.  However, it should not be
            # possible to exist in the game world with without a feature state.
            # Users are given a feature state on creation (the process is atomic).
            # This should always be do to a non-existent user.
            message: str = f"Result count was not exactly one. Received: {rows}"
            logging.debug(message)
            raise IncorrectRowCountError(message)

        for row in rows:
            name: str = row[0]
            features.add(FeatureType(name))

        return features

    def user_income_get(self, user_guid: str) -> dict[IncomeSourceType, UserIncome]:
        """
        Get user income sources
        # TODO: This can not tell if there are no stores, or if the user just doesn't exist.

        Parameters
        ----------
        user_guid: str
            The target user guid.

        Returns
        -------
        user_incomes: dict[IncomeSourceType, UserIncome]
        """

        income_sources: dict[IncomeSourceType, UserIncome] = {}

        args: list[str] = [
            user_guid,
        ]
        rows: list[Tuple[int, str, Optional[str]]] = self._call_proc("getUserIncomeByGUID", args)
        for row in rows:
            income_sources[IncomeSourceType(row[1])] = UserIncome(
                amount=row[0], name=IncomeSourceType(row[1]), description=row[2]
            )
        return income_sources

    def user_income_set(self, user_guid: str, transaction: UserIncomeSetRequest) -> None:
        """
        Set user income source.
        TODO: This needs to return more detail on success / failure.

        Parameters
        ----------
        user_guid: str
            The target user guid.
        transaction: UserIncomeSetRequest
            The user income set request.
        """

        args = [user_guid, transaction.income_source_name, transaction.amount]
        self._call_proc("deltaUserIncomeByNameAndGUID", args)

    def user_merchant_transforms_get(self, user_guid: str) -> set[StoreType]:
        """
        Get User merchant transforms [currently available].

        Parameters
        ----------
        user_guid: str
            The target user guid.

        Returns
        -------
        user_merchants: set[StoreType]
            User merchants object.
        """

        merchants: set[StoreType] = set()

        args: list = [
            user_guid,
        ]
        rows: list[Tuple[str]] = self._call_proc("getUserMerchantTransformsByGUID", args)
        for row in rows:
            merchants.add(StoreType(row[0]))
        return merchants

    def user_notifications_get(self, user_guid: str) -> list[UserNotification]:
        """
        Get User notifications.
        Returns the most recent (new) user notifications.

        Parameters
        ----------
        user_guid: str
            The target user guid.

        Returns
        -------
        user_notifications: UserNotifications
            New user notifications.
        """

        notifications: list[UserNotification] = []

        args: list = [
            user_guid,
        ]
        rows: list[Tuple[int, datetime, str]] = self._call_proc("getUserNotificationByGUID", args)
        for row in rows:
            notification: UserNotification = UserNotification(
                index=row[0], timestamp=row[1], event=UserEvent.parse_raw(row[2])
            )
            notifications.append(notification)
        return notifications

    def user_population_by_guid_get(self, user_guid: str) -> int:
        """
        Get user population (by GUID)

        Parameters
        ----------
        user_guid: str
            The target user guid.

        Returns
        -------
        user_population: int
            User population size.
        """

        rows: list[Tuple[int]] = self._call_proc(
            "getUserPopulationByGUID",
            [
                user_guid,
            ],
        )
        if rows is None or len(rows) != 1:
            message: str = f"Result count was not exactly one. Received: {rows}"
            logging.debug(message)
            raise IncorrectRowCountError(message)

        return rows[0][0]

    def user_stores_get(self, user_guid: str) -> dict[StoreType, UserStore]:
        """
        Get user stores.

        Parameters
        ----------
        user_guid: str
            The target user guid.

        Returns
        -------
        user_stores: dict[StoreType, UserStore]
            User Stores Object
        """

        stores: dict[StoreType, UserStore] = {}

        args: list[str, int] = [
            user_guid,
        ]
        rows: list[Tuple[str, Optional[str], int]] = self._call_proc("getUserStoresByGUID", args)
        for row in rows:
            stores[StoreType(row[0])] = UserStore(name=StoreType(row[0]), description=row[1], amount=row[2])
        return stores

    def user_transport(self, user_guid: str, location: str) -> UserFeatureState:
        """
        Perform User Transport.

        Parameters
        ----------
        user_guid: str
            The target user guid.
        location: str
            The name of the feature/location to transport the user to.

        Returns
        -------
        user_feature: UserFeatureState
            The active user feature state.
        """

        args: list = [user_guid, location]
        rows: list[Tuple[str, Optional[str]]] = self._call_proc("transportUserByGUID", args, True)
        if len(rows) != 1:
            # User did not exist (received an empty tuple)
            message: str = f"Result count was not exactly one. Received: {rows}"
            logging.debug(message)
            raise IncorrectRowCountError(message)
        return UserFeatureState(details=rows[0][0], description=rows[0][1])

    # Utility functions

    def process_action_queue(self, action_queue: ActionQueue) -> None:
        """
        Process the provided action queue.

        Parameters
        ----------
        action_queue: ActionQueue
            The action queue to process.
        """

        for action in action_queue.queue:
            self._call_proc(action.name, action.arguments)

    # pylint: disable=duplicate-code
    def _call_proc(self, name: str, args: list, debug: bool = False) -> Optional[list[Tuple]]:
        """
        Perform a stored procedure call.

        Parameters
        ----------
        name: str
            The name of the stored procedure to call.
        args: list
            The arguments to pass to the stored procedure.
        debug: bool
            Whether to log debug details about the call.

        Returns
        -------
        results: Optional[list[Tuple]]
            An optional list of tuples (rows) from the call.
        """

        if debug:
            logging.debug("[DAO] [Stored Proc Call Details] Name: {%s}, Arguments: {%s}", name, args)
        rows: Optional[list[Tuple]] = None
        cnx: Optional[PooledMySQLConnection] = None
        try:
            cnx = self.cnxpool.get_connection()
            cursor = cnx.cursor()
            cursor.callproc(name, args)
            for result in cursor.stored_results():
                rows = result.fetchall()
            cursor.close()
            cnx.close()
        except socket.error as error:
            logging.error("socket.error")
            logging.error(error)
            if cnx:
                cnx.close()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error"
            ) from error
        except mysql.connector.Error as error:
            logging.error("mysql.connector.Error: {%i}", error.errno)
            logging.error(str(error))
            if cnx:
                cnx.close()
            # pylint: disable=no-else-raise
            if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logging.error("Something is wrong with your user name or password")
                raise SqlExceptionError("Bad username or password") from error
            elif error.errno == errorcode.ER_BAD_DB_ERROR:
                logging.error("Database does not exist")
                raise SqlExceptionError("Database does not exist") from error
            elif error.errno == errorcode.ER_DUP_ENTRY:
                logging.error("Duplicate key")
                raise DuplicateKeyError(str(error)) from error
            raise SqlExceptionError(f"Unhandled SQL Exception: {str(error)}") from error
        except Exception as error:
            logging.error("error")
            # All other uncaught exception types
            logging.error(str(error))
            if cnx:
                cnx.close()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error"
            ) from error

        if debug:
            logging.debug("[DAO] [Stored Proc Call Details] Returning:")
            logging.debug(rows)
        return rows
