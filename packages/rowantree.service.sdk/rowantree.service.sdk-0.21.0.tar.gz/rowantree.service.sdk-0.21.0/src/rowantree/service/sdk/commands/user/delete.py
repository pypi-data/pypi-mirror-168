""" User Delete Command Definition """

from starlette import status

from rowantree.common.sdk import demand_env_var

from ...contracts.dto.request_status_codes import RequestStatusCodes
from ...contracts.dto.wrapped_request import WrappedRequest
from ...contracts.request_verb import RequestVerb
from ..abstract_command import AbstractCommand


class UserDeleteCommand(AbstractCommand):
    """
    User Delete Command
    Deletes a user.

    Methods
    -------
    execute(self, user_guid: str) -> None
        Executes the command.
    """

    def execute(self, user_guid: str) -> None:
        """
        Executes the command.

        Parameters
        ----------
        user_guid: str
            The target user guid.
        """

        request: WrappedRequest = WrappedRequest(
            verb=RequestVerb.DELETE,
            url=f"{demand_env_var(name='ROWANTREE_SERVICE_ENDPOINT')}/v1/user/{user_guid}",
            statuses=RequestStatusCodes(allow=[status.HTTP_200_OK], reauth=[status.HTTP_401_UNAUTHORIZED], retry=[]),
        )
        self.wrapped_request(request=request)
