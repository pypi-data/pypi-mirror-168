""" User State Get Controller Definition """

from starlette import status
from starlette.exceptions import HTTPException

from rowantree.contracts import (
    FeatureType,
    IncomeSourceType,
    StoreType,
    UserFeatureState,
    UserIncome,
    UserNotification,
    UserState,
    UserStore,
)

from ..services.db.incorrect_row_count_error import IncorrectRowCountError
from .abstract_controller import AbstractController


class UserStateGetController(AbstractController):
    """
    User State Get Controller
    Gets the user game state.

    Methods
    -------
    execute(self, user_guid: str) -> UserState
        Executes the command.
    """

    def execute(self, user_guid: str) -> UserState:
        """
        Gets the user game state.

        Parameters
        ----------
        user_guid: str
            The target user guid.

        Returns
        -------
        user_state: UserState
            The user state object.
        """

        try:
            # User Game State
            active: int = self.dao.user_active_state_get(user_guid=user_guid)

            # User Stores (Inventory)
            stores: dict[StoreType, UserStore] = self.dao.user_stores_get(user_guid=user_guid)

            # User Income
            incomes: dict[IncomeSourceType, UserIncome] = self.dao.user_income_get(user_guid=user_guid)

            # Features
            features: set[FeatureType] = self.dao.user_features_get(user_guid=user_guid)

            # Population
            population: int = self.dao.user_population_by_guid_get(user_guid=user_guid)

            # Active Feature Details and name
            active_feature_state: UserFeatureState = self.dao.user_active_feature_state_details_get(user_guid=user_guid)
            active_feature_state.name = self.dao.user_active_feature_get(user_guid=user_guid)

            # Merchants
            merchants: set[StoreType] = self.dao.user_merchant_transforms_get(user_guid=user_guid)

            # Notifications
            notifications: list[UserNotification] = self.dao.user_notifications_get(user_guid=user_guid)

        except IncorrectRowCountError as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found") from error

        user_state: UserState = UserState(
            active=active,
            stores=stores,
            incomes=incomes,
            features=features,
            active_feature_state=active_feature_state,
            population=population,
            merchants=merchants,
            notifications=notifications,
        )
        return user_state
