""" Abstract Command Definition """
import json
import logging
import time
from abc import abstractmethod
from typing import Any, Optional

import requests
from requests import Response

from rowantree.common.sdk import demand_env_var, demand_env_var_as_float, demand_env_var_as_int
from rowantree.contracts import BaseModel

from ..contracts.dto.command_options import CommandOptions
from ..contracts.dto.wrapped_request import WrappedRequest
from ..contracts.exceeded_retry_count_error import ExceededRetryCountError
from ..contracts.request_failure_error import RequestFailureError
from ..contracts.request_verb import RequestVerb


class AbstractCommand(BaseModel):
    """
    Abstract Command
    """

    options: Optional[CommandOptions]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.options is None:
            self.options = CommandOptions(
                sleep_time=demand_env_var_as_float(name="ACCESS_AUTH_ENDPOINT_SLEEP_TIME"),
                retry_count=demand_env_var_as_int(name="ACCESS_AUTH_ENDPOINT_RETRY_COUNT"),
                tld=demand_env_var(name="ROWANTREE_TLD"),
                timeout=demand_env_var_as_float(name="ACCESS_AUTH_ENDPOINT_TIMEOUT"),
            )

    @abstractmethod
    def execute(self, *args, **kwargs) -> Optional[Any]:
        """Command entry point"""

    def _build_requests_params(self, request: WrappedRequest) -> dict:
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
            "timeout": self.options.timeout,
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
            raise ExceededRetryCountError(json.dumps({"request": request.dict(by_alias=True), "depth": depth}))
        depth -= 1

        params: dict = self._build_requests_params(request=request)
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
            time.sleep(self.options.sleep_time)
            return self._api_caller(request=request, depth=depth)
        except Exception as error:
            logging.debug("Exception needed to cover: %s", str(error))
            time.sleep(self.options.sleep_time)
            return self._api_caller(request=request, depth=depth)

        if response.status_code in request.statuses.allow:
            return response.json()

        if response.status_code in request.statuses.retry:
            time.sleep(self.options.sleep_time)
            return self._api_caller(request=request, depth=depth)

        raise RequestFailureError(
            json.dumps({"status_code": response.status_code, "request": request.dict(by_alias=True), "depth": depth})
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

        return self._api_caller(request=request, depth=self.options.retry_count)
