""" Abstract Command Definition """
import json
import logging
import time
from abc import abstractmethod
from typing import Any, Optional

import requests
from requests import Response

from rowantree.auth.sdk import AuthenticateUserCommand, AuthenticateUserRequest, Token
from rowantree.common.sdk import demand_env_var, demand_env_var_as_float
from rowantree.contracts import BaseModel

from ..contracts.dto.wrapped_request import WrappedRequest
from ..contracts.exceeded_retry_count_error import ExceededRetryCountError
from ..contracts.request_failure_error import RequestFailureError
from ..contracts.request_verb import RequestVerb

# Acts as a singleton for auth across multiple commands.
ROWANTREE_SERVICE_SDK_HEADERS: dict[str, str] = {}


class AbstractCommand(BaseModel):
    """
    Abstract Command

    Attributes
    ----------
    timeout: float = 30
        The default timeout of requests.
    """

    sleep_time: float = 1
    retry_count: int = 5
    authenticate_user_command: AuthenticateUserCommand = AuthenticateUserCommand()

    def __init__(self, **data: Any):
        super().__init__(**data)
        # If we are the first to need the singleton, then create it.
        if "Authorization" not in ROWANTREE_SERVICE_SDK_HEADERS:
            self._authenticate()

    @abstractmethod
    def execute(self, *args, **kwargs) -> Optional[Any]:
        """Command entry point"""

    # User Commands
    def _authenticate(self) -> None:
        """
        Authenticates the session.

        This method writes into ROWANTREE_SERVICE_SDK_HEADERS which is acting as a singleton
        for use across all service sdk commands.
        """

        request: AuthenticateUserRequest = AuthenticateUserRequest(
            username=demand_env_var(name="ACCESS_USERNAME"), password=demand_env_var(name="ACCESS_PASSWORD")
        )
        auth_token: Token = self.authenticate_user_command.execute(request=request)
        ROWANTREE_SERVICE_SDK_HEADERS["Authorization"] = f"Bearer {auth_token.access_token}"

    @staticmethod
    def _build_requests_params(request: WrappedRequest) -> dict:
        """
        Builds the `requests` call parameters.

        Parameters
        ----------
        request: WrappedRequest
            The request to make.

        Returns
        -------
        params: dict
            A dictionary suitable for splatting into the `requests` call.
        """

        params: dict = {
            "url": request.url,
            "headers": ROWANTREE_SERVICE_SDK_HEADERS,
            "timeout": demand_env_var_as_float(name="ROWANTREE_SERVICE_TIMEOUT"),
        }
        if request.verb == RequestVerb.POST:
            params["data"] = request.data
        if request.params is not None:
            params["params"] = request.params
        return params

    def _api_caller(self, request: WrappedRequest, depth: int) -> dict:
        """
        Wrapper for calls with `requests` to external APIs.

        Parameters
        ----------
        request: WrappedRequest
            Request to make.
        depth: int
            Call depth of the recursive call (retry)

        Returns
        -------
        response: dict
            A dictionary of the response.
        """

        if depth < 1:
            raise ExceededRetryCountError(json.dumps({"request": request.dict(), "depth": depth}))
        depth -= 1

        params: dict = AbstractCommand._build_requests_params(request=request)
        # pylint: disable=broad-except
        try:
            if request.verb == RequestVerb.GET:
                response: Response = requests.get(**params)
            elif request.verb == RequestVerb.POST:
                response: Response = requests.post(**params)
            elif request.verb == RequestVerb.DELETE:
                response: Response = requests.delete(**params)
            else:
                raise Exception("Unknown Verb")
        except requests.exceptions.ConnectionError as error:
            logging.debug("Connection Error (%s) - Retrying.. %i", str(error), depth)
            time.sleep(self.sleep_time)
            return self._api_caller(request=request, depth=depth)
        except Exception as error:
            logging.debug("Exception needed to cover: %s", str(error))
            time.sleep(self.sleep_time)
            return self._api_caller(request=request, depth=depth)

        if response.status_code in request.statuses.allow:
            return response.json()

        if response.status_code in request.statuses.retry:
            time.sleep(self.sleep_time)
            return self._api_caller(request=request, depth=depth)

        if response.status_code in request.statuses.reauth:
            self._authenticate()
            return self._api_caller(request=request, depth=depth)

        raise RequestFailureError(
            json.dumps({"status_code": response.status_code, "request": request.dict(), "depth": depth})
        )

    def wrapped_request(self, request: WrappedRequest) -> dict:
        """
        High level request method.  Entry point for consumption.


        Parameters
        ----------
        request: WrappedRequest
            The request to make.

        Returns
        -------
        response: dict
            The response as a dictionary.
        """

        return self._api_caller(request=request, depth=self.retry_count)
