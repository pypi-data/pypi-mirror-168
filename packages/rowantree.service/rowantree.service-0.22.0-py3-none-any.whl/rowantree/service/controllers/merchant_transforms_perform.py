""" Merchant Transform Perform Controller Definition """

from rowantree.service.sdk import MerchantTransformRequest

from .abstract_controller import AbstractController


class MerchantTransformPerformController(AbstractController):
    """
    Merchant Transform Perform Controller

    Methods
    -------
    execute(self, user_guid: str, request: MerchantTransformRequest) -> None
        Executes the command.
    """

    def execute(self, user_guid: str, request: MerchantTransformRequest) -> None:
        """
        Performs a merchant transform.

        Parameters
        ----------
        user_guid: str
            The target user guid.
        request: MerchantTransformRequest
            The merchant transform request.
        """

        self.dao.merchant_transform_perform(user_guid=user_guid, store_name=request.store_name)
