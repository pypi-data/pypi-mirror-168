import abc
import logging
import time
from typing import Optional, Dict, Any

import requests
from requests.adapters import HTTPAdapter, Retry

logger = logging.getLogger(__name__)


class ResistantApiException(Exception):
    pass


DEFAULT_RETRY = Retry(backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504], allowed_methods=False)


class TimeoutHTTPAdapter(HTTPAdapter):
    DEFAULT_TIMEOUT = 2.0  # seconds

    def __init__(self, *args, timeout: float = DEFAULT_TIMEOUT, **kwargs):
        self.timeout = timeout
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        response = super().send(request, **kwargs)
        return response


class ApiClientBase(abc.ABC):
    MAX_NUM_RETRIES_POLL = 10
    MAX_SLEEP_TIMEOUT = 32
    MAX_NUM_RETRIES_SUBMIT = 10

    def __init__(self, api_session: requests.Session, s3_session: requests.Session = requests.Session(),
                 max_sleep_timeout: int = MAX_SLEEP_TIMEOUT, proxy: Optional[str] = None, **kwargs) -> None:
        self._api_session = api_session
        self._s3_session = s3_session
        self.max_sleep_timeout = max_sleep_timeout
        self._s3_session.mount('https://', TimeoutHTTPAdapter(max_retries=DEFAULT_RETRY, **kwargs))
        self._api_session.mount('https://', TimeoutHTTPAdapter(max_retries=DEFAULT_RETRY, **kwargs))

        if proxy:
            self._api_session.proxies.update(https=proxy)
            self._s3_session.proxies.update(https=proxy)

    def _submit(self, url: str, data: bytes, query_id: str = "", pipeline_configuration: Optional[str] = None, enable_decision: bool = False) -> str:
        body = {"query_id": query_id}
        if pipeline_configuration:
            body['pipeline_configuration'] = pipeline_configuration
        if enable_decision:
            body['enable_decision'] = True

        response = self._api_session.post(url, json=body)
        if response.status_code == 200:
            response_data = response.json()
            response_put = self._s3_session.put(response_data["upload_url"], data=data, headers={'Content-Type': 'application/octet-stream'})
            response_put.raise_for_status()
            return response_data["submission_id"]
        else:
            response.raise_for_status()

    def _poll(self, url: str, submission_id: str, max_num_retries: int = MAX_NUM_RETRIES_POLL, query_params: Optional[Dict[str, Any]] = None) -> dict:
        sleep_timeout = 1
        for i in range(max_num_retries):
            response = self._api_session.get(url.format(submission_id=submission_id), params=query_params)
            if response.status_code == 200:
                return response.json()
            if response.status_code == 404:
                logger.info("Submission not found. Waiting for retry...%d/%d", i, max_num_retries)
                time.sleep(min(sleep_timeout, self.max_sleep_timeout))
                sleep_timeout *= 2
            else:
                response.raise_for_status()
        raise RuntimeError("Submission not found, reached max number of retries.")

    def _get_response_body(self, response: requests.Response) -> Optional[dict]:
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        else:
            response.raise_for_status()
