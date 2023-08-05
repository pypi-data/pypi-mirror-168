""" User Merchant Transforms Get Command Definition """

from starlette import status

from rowantree.common.sdk import demand_env_var
from rowantree.contracts import StoreType

from ...contracts.dto.request_status_codes import RequestStatusCodes
from ...contracts.dto.wrapped_request import WrappedRequest
from ...contracts.request_verb import RequestVerb
from ...contracts.responses.merchant_transforms_get import MerchantTransformsGetResponse
from ..abstract_command import AbstractCommand


class UserMerchantTransformsGetCommand(AbstractCommand):
    """
    User Merchant Transforms Get Command
    Gets a (unique) list of user merchant transforms.

    Methods
    -------
    execute(self, user_guid: str) -> set[StoreType]
        Executes the command.
    """

    def execute(self, user_guid: str) -> set[StoreType]:
        """
        Executes the command.

        Parameters
        ----------
        user_guid: str
            Target user guid.

        Returns
        -------
        user_merchants: set[StoreType]
            The (unique) set of user merchants.
        """

        request: WrappedRequest = WrappedRequest(
            verb=RequestVerb.GET,
            url=f"{demand_env_var(name='ROWANTREE_SERVICE_ENDPOINT')}/v1/user/{user_guid}/merchant",
            statuses=RequestStatusCodes(allow=[status.HTTP_200_OK], reauth=[status.HTTP_401_UNAUTHORIZED], retry=[]),
        )
        response: dict = self.wrapped_request(request=request)
        merchant_transforms_get_response: MerchantTransformsGetResponse = MerchantTransformsGetResponse.parse_obj(
            response
        )
        return merchant_transforms_get_response.merchants
