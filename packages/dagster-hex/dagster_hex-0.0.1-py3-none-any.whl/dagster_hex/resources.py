import datetime
import logging
import time
from importlib.metadata import PackageNotFoundError, version
from typing import Any, Dict, Optional, cast
from urllib.parse import urljoin

import requests
from dagster import Failure, Field, StringSource, get_dagster_logger, resource

from .consts import (
    COMPLETE,
    DEFAULT_POLL_INTERVAL,
    DEFAULT_POLL_TIMEOUT,
    HEX_API_BASE,
    TERMINAL_STATUSES,
    VALID_STATUSES,
)
from .types import HexOutput, RunResponse, StatusResponse


class HexResource:
    """
    This class exposes methods on top of the Hex REST API.

    :param api_key: Hex API Token to use for authentication
    :type api_key: str
    :param base_url: Base URL for the API
    :type: base_url: str
    :param request_max_retries: Number of times to retry a failed request
    :type request_max_retries: int
    :number request_retry_delay: Time, in seconds, to wait between retries
    :type request_retry_delay: int
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = HEX_API_BASE,
        log: logging.Logger = get_dagster_logger(),
        request_max_retries: int = 3,
        request_retry_delay: float = 0.25,
    ):

        self._log = log
        self._api_key = api_key
        self._request_max_retries = request_max_retries
        self._request_retry_delay = request_retry_delay
        self.api_base_url = base_url

    def make_request(
        self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Creates and sends a request to the desired Hex API endpoint

        Args:
            method (str): The http method use for this request (e.g. "GET", "POST").
            endpoint (str): The Hex API endpoint to send this request to.
            data (Optional(dict): Query parameters to pass to the API endpoint

        Returns:
            Dict[str, Any]: Parsed json data from the response to this request
        """

        try:
            __version__ = version("dagster_hex")
        except PackageNotFoundError:
            __version__ = "UnknownVersion"

        user_agent = "HexDagsterOp/" + __version__
        headers = {"Authorization": f"Bearer {self._api_key}", "User-Agent": user_agent}
        url = urljoin(self.api_base_url, endpoint)

        num_retries = 0
        while True:
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=data,
                )
                response.raise_for_status()
                if response.headers.get("Content-Type", "").startswith(
                    "application/json"
                ):
                    try:
                        response_json = response.json()
                    except requests.exceptions.JSONDecodeError:
                        self._log.error("Failed to decode response from API.")
                        self._log.error("API returned: %s", response.text)
                        raise Failure(
                            "Unexpected response from Hex API.Failed to decode to JSON."
                        )
                    return response_json
            except requests.RequestException as e:
                self._log.error("Request to Hex API failed: %s", e)
                if num_retries == self._request_max_retries:
                    break
                num_retries += 1
                time.sleep(self._request_retry_delay)

        raise Failure("Exceeded max number of retries.")

    def run_project(
        self,
        project_id: str,
        inputs: Optional[Dict[str, Any]] = None,
        update_cache: bool = False,
    ) -> RunResponse:
        """Trigger a sync and initiate a sync run

        Args:
            project_id (str): The Hex Project ID
            inputs (dict): additional input parameters, a json-serializable dictionary
                of variable_name: value pairs.
            update_cache (bool): When true, this run will update the cached state of the
                published app with the latest run results.
                Additionally, any SQL cells that have caching enabled will be
                re-executed as part of this run. Note that this cannot be set to true
                if custom input parameters are provided.

        Returns:
            RunResponse
        """
        method = "POST"
        endpoint = f"/api/v1/project/{project_id}/run"
        response = cast(
            RunResponse,
            self.make_request(
                method=method,
                endpoint=endpoint,
                data={"inputParams": inputs, "updateCache": update_cache},
            ),
        )
        return response

    def run_status(self, project_id, run_id) -> StatusResponse:
        endpoint = f"api/v1/project/{project_id}/run/{run_id}"
        method = "GET"

        response = cast(
            StatusResponse,
            self.make_request(method=method, endpoint=endpoint, data=None),
        )
        return response

    def cancel_run(self, project_id, run_id) -> str:
        endpoint = f"api/v1/project/{project_id}/run/{run_id}"
        method = "DELETE"

        self.make_request(method=method, endpoint=endpoint)
        return run_id

    def run_and_poll(
        self,
        project_id: str,
        inputs: Optional[dict],
        update_cache: bool = False,
        kill_on_timeout: bool = True,
        poll_interval: float = DEFAULT_POLL_INTERVAL,
        poll_timeout: Optional[float] = DEFAULT_POLL_TIMEOUT,
    ) -> HexOutput:
        """Trigger a project and poll until complete

        Args:
            project_id (str): The Hex project id
            inputs (dict) additional input parameters, a json-serializable dictionary
                of variable_name: value pairs.
            update_cache (bool): When true, this run will update the cached state of the
                published app with the latest run results.
                Additionally, any SQL cells that have caching enabled will be
                re-executed as part of this run. Note that this cannot be set to true
                if custom input parameters are provided.
            kill_on_timeout (bool): attempt to stop the project if the timeout is
                reached. If false, the project will continue running indefinitely in the
                background until completion.
            poll_interval (int): time to wait in between polls to the API
            poll_timeout (int): maximum time to wait for the project to complete

        Returns:
            Dict[str, Any]: Parsed json output from the API
        """
        run_response = self.run_project(project_id, inputs, update_cache)
        run_id = run_response["runId"]
        poll_start = datetime.datetime.now()
        while True:
            run_status = self.run_status(project_id, run_id)
            project_status = run_status["status"]

            self._log.debug(run_status)
            self._log.info(
                f"Polling Hex Project {project_id}. Current status: {project_status}."
            )

            if project_status not in VALID_STATUSES:
                raise Failure(
                    f"Received an unexpected status from the API: {project_status}"
                )

            if project_status == COMPLETE:
                break

            if project_status in TERMINAL_STATUSES:
                raise Failure(
                    f"Project Run failed with status {project_status}. "
                    f"See Run URL for more info {run_response['runUrl']}"
                )

            if (
                poll_timeout
                and datetime.datetime.now()
                > poll_start + datetime.timedelta(seconds=poll_timeout)
            ):
                if kill_on_timeout:
                    self.cancel_run(project_id, run_id)
                raise Failure(
                    f"Project {project_id} for run: {run_id}' timed out after "
                    f"{datetime.datetime.now() - poll_start}. "
                    f"Last status was {project_status}. "
                    f"TraceId: {run_status['traceId']}"
                )

            time.sleep(poll_interval)
        return HexOutput(run_response=run_response, status_response=run_status)


@resource(
    config_schema={
        "api_key": Field(
            StringSource,
            is_required=True,
            description="Hex API Key. You can find this on the Hex settings page",
        ),
        "base_url": Field(
            StringSource,
            default_value="https://app.hex.tech",
            description="Hex Base URL for API requests.",
        ),
        "request_max_retries": Field(
            int,
            default_value=3,
            description="The maximum times requests to the Hex API should be retried "
            "before failing.",
        ),
        "request_retry_delay": Field(
            float,
            default_value=0.25,
            description="Time (in seconds) to wait between each request retry.",
        ),
    },
    description="This resource helps manage Hex",
)
def hex_resource(context) -> HexResource:
    """
    This resource allows users to programmatically interface with the Hex REST API
    """
    return HexResource(
        api_key=context.resource_config["api_key"],
        base_url=context.resource_config["base_url"],
        log=context.log,
        request_max_retries=context.resource_config["request_max_retries"],
        request_retry_delay=context.resource_config["request_retry_delay"],
    )
