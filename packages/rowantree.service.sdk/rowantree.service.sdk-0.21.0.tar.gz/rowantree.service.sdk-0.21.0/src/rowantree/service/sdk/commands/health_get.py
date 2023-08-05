""" Health Get Command Definition """

import requests
from requests import Response

from rowantree.common.sdk import demand_env_var, demand_env_var_as_float

from .abstract_command import AbstractCommand


class HealthGetCommand(AbstractCommand):
    """
    Health Get Command
    Gets the server health.

    Methods
    -------
    execute(self) -> bool
        Executes the command.
    """

    def execute(self) -> bool:
        """
        Executes the command.

        Returns
        -------
        health: bool
            The server health (true or false).
        """

        response: Response = requests.get(
            url=f"{demand_env_var(name='ROWANTREE_SERVICE_ENDPOINT')}/health/plain",
            timeout=demand_env_var_as_float(name="ROWANTREE_SERVICE_TIMEOUT"),
        )
        return bool(response.text)
