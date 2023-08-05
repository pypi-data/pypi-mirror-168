""" World Status Get Command Definition """

from starlette import status

from rowantree.common.sdk import demand_env_var

from ..contracts.dto.request_status_codes import RequestStatusCodes
from ..contracts.dto.world_status import WorldStatus
from ..contracts.dto.wrapped_request import WrappedRequest
from ..contracts.request_verb import RequestVerb
from .abstract_command import AbstractCommand


class WorldStatusGetCommand(AbstractCommand):
    """
    World Status Get Command
    Gets the world status.

    Methods
    -------
    execute(self) -> WorldStatus
        Executes the command.
    """

    def execute(self) -> WorldStatus:
        """
        Executes the command.

        Returns
        -------
        world_status: WorldStatus
            The world status.
        """

        request: WrappedRequest = WrappedRequest(
            verb=RequestVerb.GET,
            url=f"{demand_env_var(name='ROWANTREE_SERVICE_ENDPOINT')}/v1/world",
            statuses=RequestStatusCodes(allow=[status.HTTP_200_OK], reauth=[status.HTTP_401_UNAUTHORIZED], retry=[]),
        )
        response: dict = self.wrapped_request(request=request)
        return WorldStatus.parse_obj(response)
