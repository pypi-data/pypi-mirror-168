""" User Income Set Command Definition """

from starlette import status

from rowantree.common.sdk import demand_env_var

from ...contracts.dto.request_status_codes import RequestStatusCodes
from ...contracts.dto.wrapped_request import WrappedRequest
from ...contracts.request_verb import RequestVerb
from ...contracts.requests.user.income_set import UserIncomeSetRequest
from ..abstract_command import AbstractCommand


class UserIncomeSetCommand(AbstractCommand):
    """
    User Income Set Command
    Sets a user income. (Creates or dismisses a number of workers of the type).

    Methods
    -------
    execute(self, user_guid: str, request: UserIncomeSetRequest) -> None
        Executes the command.
    """

    def execute(self, request: UserIncomeSetRequest) -> None:
        """
        Executes the command.

        Parameters
        ----------
        request: UserIncomeSetRequest
            The UserIncomeSetRequest object for the update.
        """

        request: WrappedRequest = WrappedRequest(
            verb=RequestVerb.POST,
            url=f"{demand_env_var(name='ROWANTREE_SERVICE_ENDPOINT')}/v1/user/{request.user_guid}/income",
            statuses=RequestStatusCodes(allow=[status.HTTP_200_OK], reauth=[status.HTTP_401_UNAUTHORIZED], retry=[]),
            data=request.json(by_alias=True, exclude={"user_guid"}),
        )
        self.wrapped_request(request=request)
