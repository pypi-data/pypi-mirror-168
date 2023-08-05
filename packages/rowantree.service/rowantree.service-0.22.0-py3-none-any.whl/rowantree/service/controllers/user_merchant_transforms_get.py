""" User Merchant Transforms Get Controller Definition """
from rowantree.contracts import StoreType
from rowantree.service.sdk import MerchantTransformsGetResponse

from .abstract_controller import AbstractController


class UserMerchantTransformsGetController(AbstractController):
    """
    User Merchant Transforms Get Controller
    Gets a (unique) list of user merchant transforms.

    Methods
    -------
    execute(self, user_guid: str) -> UserMerchants
        Executes the command.
    """

    def execute(self, user_guid: str) -> MerchantTransformsGetResponse:
        """
        Gets a (unique) list of user merchant transforms.

        Parameters
        ----------
        user_guid: str
            Target user guid.

        Returns
        -------
        user_merchants: MerchantTransformsGetResponse
            A (unique) list of user merchant transforms.
        """

        merchants: set[StoreType] = self.dao.user_merchant_transforms_get(user_guid=user_guid)
        return MerchantTransformsGetResponse(merchants=merchants)
