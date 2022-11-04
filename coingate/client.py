import posixpath
from ast import With
from typing import Any, Dict, Optional, Union

from .http_client import HTTPClient
from .services import (
    LedgerService,
    OrderService,
    PublicService,
    RefundService,
    WithdrawalService,
)


class CoinGate:
    BASE_API_URL = "https://api.coingate.com"
    BASE_SANDBOX_API_URL = "https://api-sandbox.coingate.com"

    def __init__(
        self, api_key: Optional[str] = None, use_sanbox_mode: bool = False
    ) -> None:
        self._http_client = HTTPClient(api_key)
        self._use_sandbox_mode = use_sanbox_mode

        self._order = OrderService(self)
        self._refund = RefundService(self)
        self._public = PublicService(self)
        self._ledger = LedgerService(self)
        self._withdrawal = WithdrawalService(self)

    @property
    def order(self) -> OrderService:
        return self._order

    @property
    def refund(self) -> RefundService:
        return self._refund

    @property
    def public(self) -> PublicService:
        return self._public

    @property
    def ledger(self) -> LedgerService:
        return self._ledger

    @property
    def withdrawal(self) -> WithdrawalService:
        return self._withdrawal

    @property
    def is_sandbox_mode(self):
        return self._use_sandbox_mode

    def set_api_key(self, api_key: Optional[str]):
        self._http_client.api_key = api_key

    def set_timeout(self, timeout: Optional[int]):
        self._http_client.timeout = timeout

    def set_app_info(self, name: str, *, version: str):
        self._http_client.update_user_agent(name=name, version=version)

    def request(
        self,
        method: Union[str, bytes],
        endpoint: str,
        *,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ):
        url = self._build_path_to_endpoint(endpoint)
        return self._http_client.request(method, url, data=data, params=params)

    def _base_api_url(self):
        return self.BASE_SANDBOX_API_URL if self.is_sandbox_mode else self.BASE_API_URL

    def _build_path_to_endpoint(self, endpoint: str) -> str:
        api_url = self._base_api_url()
        endpoint = endpoint.lower()
        return posixpath.join(api_url, endpoint)
