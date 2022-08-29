from typing import Any, Optional, Union

import requests

from . import exceptions


class HTTPClient:
    def __init__(self, api_key: Optional[str]) -> None:
        self._api_key = api_key
        self._session = requests.Session()
        self._timeout: Optional[int] = 60

        if api_key is not None:
            self._update_auth_headers(api_key)

    @property
    def api_key(self) -> Optional[str]:
        return self._api_key

    @api_key.setter
    def api_key(self, value: Optional[str]) -> None:
        self._update_auth_headers(value)

    @property
    def timeout(self) -> Optional[int]:
        return self._timeout

    @timeout.setter
    def timeout(self, value: Optional[int]) -> None:
        self._timeout = value

    def _update_auth_headers(self, value: Optional[str]) -> None:
        self._session.headers.update({"Authorization": f"Token {value}"})

    def request(
        self,
        method: Union[str, bytes],
        url: Union[str, bytes],
        *,
        data: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
    ) -> requests.Response:
        headers = {}
        if method in ("post", "patch") or data is not None:
            headers.update({"Content-Type": "application/x-www-form-urlencoded"})

        response = self._session.request(
            method,
            url,
            data=data,
            params=params,
            timeout=self._timeout,
            headers=headers,
        )
        return self._process_response(response)

    def _process_response(self, response: requests.Response):
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            client_exception = self._raise_client_error(response)
            raise client_exception or e
        else:
            return response

    def _raise_client_error(self, response: requests.Response):
        try:
            body = response.json()
            reason = body.get("reason")
            message = body.get("message")
            errors = body.get("errors")
            exception = (
                getattr(exceptions, f"{reason}Exception", None)
                or exceptions.ApiException
            )

            return exception(
                reason=reason,
                status_code=response.status_code,
                message=message,
                errors=errors,
            )
        except ValueError:
            return None
