""" User Feature Active Get Command """
from starlette import status

from rowantree.common.sdk import demand_env_var
from rowantree.contracts import UserFeatureState

from ...contracts.dto.request_status_codes import RequestStatusCodes
from ...contracts.dto.wrapped_request import WrappedRequest
from ...contracts.request_verb import RequestVerb
from ..abstract_command import AbstractCommand


class UserFeatureActiveGetCommand(AbstractCommand):
    """
    User Feature Active Get Command
    Gets the active user feature.

    Methods
    -------
    execute(self, user_guid: str, details: bool) -> FeatureType
        Executes the command.
    """

    def execute(self, user_guid: str) -> UserFeatureState:
        """
        Executes the command.

        Parameters
        ----------
        user_guid: str
            The target user guid.

        Returns
        -------
        user_feature: UserFeatureState
            The active UserFeatureState.
        """

        request: WrappedRequest = WrappedRequest(
            verb=RequestVerb.GET,
            url=f"{demand_env_var(name='ROWANTREE_SERVICE_ENDPOINT')}/v1/user/{user_guid}/features/active",
            statuses=RequestStatusCodes(allow=[status.HTTP_200_OK], reauth=[status.HTTP_401_UNAUTHORIZED], retry=[]),
        )
        response: dict = self.wrapped_request(request=request)
        return UserFeatureState.parse_obj(response)
