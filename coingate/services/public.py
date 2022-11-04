from decimal import Decimal
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from typing_extensions import Literal

from ..resources.public import (
    ExchangesRates,
    ExchangeTrader,
    NestedCurrencyObject,
    Ping,
    PublicCurrency,
    PublicPlatform,
)

if TYPE_CHECKING:
    from ..client import CoinGate


class PublicService:
    def __init__(self, client: "CoinGate"):
        self._client = client

    def get_exchange_rate_for_merchant(
        self, from_currency: str, to_currency: str
    ) -> Optional[Decimal]:
        """Get current exchange rate for any two currencies for merchant, fiat or crypto

        :param str `from_currency`: ISO Symbol. Example: EUR, USD, BTC, ETH, etc
        :param str `to_currency`: ISO Symbol. Example: EUR, USD, BTC, ETH, etc

        :rtype Decimal

        Basic Usage::

          >>> client = CoinGate()
          >>> client.public.get_exchange_rate_for_merchant("ETH", "EUR")

        """
        return self._get_exchange_rate("merchant", from_currency, to_currency)

    def get_exchange_rate_for_trader(
        self, kind: Literal["buy", "sell"], from_currency: str, to_currency: str
    ) -> Optional[Decimal]:
        """Get current exchange rate for any two currencies for trader, fiat or crypto

        :param Literal["buy", "sell"] `kind`
        :param str `from_currency`: ISO Symbol. Example: EUR, USD, BTC, ETH, etc
        :param str `to_currency`: ISO Symbol. Example: EUR, USD, BTC, ETH, etc

        :rtype Decimal

        Basic Usage::

          >>> client = CoinGate()
          >>> client.public.get_exchange_rate_for_trader("buy", "ETH", "EUR")

        """
        return self._get_exchange_rate(f"trader/{kind}", from_currency, to_currency)

    def _get_exchange_rate(
        self, sideType: str, from_currency: str, to_currency: str
    ) -> Optional[Decimal]:
        response = self._client.request(
            "get", f"v2/rates/{sideType}/{from_currency}/{to_currency}"
        ).text

        return Decimal(response) if len(response) else None

    def get_all_exchange_rates(self) -> ExchangesRates:
        """Get current CoinGate exchange rates for Merchants and Traders

        :rtype: :class:`<coingate.resources.public.ExchangeRates>`

        Basic Usage::
          >>> client = CoinGate()
          >>> client.public.get_all_exchange_rates()

        """
        response = self._get_exchange_rates()
        return ExchangesRates(**response)

    def get_merchant_exchange_rates(self) -> NestedCurrencyObject:
        """Get current CoinGate exchange rates for Merchant

        :rtype: `:class:`<coingate.resources.public.NestedCurrencyObject>`

        Basic Usage::
          >>> client = CoinGate()
          >>> client.public.get_merchant_exchange_rates()

        """
        response = self._get_exchange_rates("merchant")
        return NestedCurrencyObject(response)

    def get_trader_exchange_rates(
        self, kind: Optional[Literal["buy", "sell"]] = None
    ) -> Union[ExchangeTrader, NestedCurrencyObject]:
        """Get current CoinGate exchange rates for Trader

        :param Optional[Literal["buy", "sell"]]

        :rtype: Union[`:class:`<coingate.resources.ExchangeTrader>`, `:class:`<coingate.resources.NestedCurrencyObject>`]

        Basic Usage::
          >>> client = CoinGate()
          >>> client.public.get_trader_exchange_rates("buy")

        """
        sideType = "trader" if kind is None else f"trader/{kind}"
        response = self._get_exchange_rates(sideType)
        return (
            ExchangeTrader(**response)
            if kind is None
            else NestedCurrencyObject(response)
        )

    def _get_exchange_rates(self, sideType: Optional[str] = None) -> Dict[str, Any]:
        endpoint = "v2/rates" if sideType is None else f"v2/rates/{sideType}"
        return self._client.request("get", endpoint).json()

    def ping(self) -> Ping:
        """A health check endpoint for CoinGate API

        :rtype :class:`<coingate.resources.public.Ping>`

        Basic Usage::
          >>> client = CoinGate()
          >>> client.public.ping()

        """
        response = self._client.request("get", "v2/ping").json()
        return Ping(**response)

    def get_ip_addresses(self, separator: Optional[str] = None) -> str:
        """Get IP addresses of CoinGate servers

        :param Optional[str] `separator`: Separator of ip addresses. Default new line (\\n).

        :rtype str

        Basic Usage::
          >>> client = CoinGate()
          >>> client.public.get_ip_addresses(separator="|")

        """

        return self._client.request(
            "get", "v2/ips-v4", params={"separator": separator}
        ).text

    def get_currencies(
        self,
        native: bool,
        enabled: bool,
        merchant_pay: bool,
        merchant_receive: bool,
        kind: Literal["crypto", "fiat"],
    ) -> List[PublicCurrency]:
        """Retrieves all currencies.

        :param bool `native`
        :param bool `enabled`
        :param bool `merchant_pay`
        :param bool `merchant_receive`
        :param Literal["crypto", "fiat"] `kind`

        :rtype List[:class:`<coingate.resources.public.PublicCurrency>`]

        Basic Usage::
          >>> client = CoinGate()
          >>> client.public.get_currencies()

        """
        response = self._client.request(
            "get",
            "v2/currencies",
            params={
                "native": native,
                "enabled": enabled,
                "merchant_pay": merchant_pay,
                "merchant_receive": merchant_receive,
                "kind": kind,
            },
        ).json()

        return [PublicCurrency(**currency) for currency in response]

    def get_platforms(self, enabled: bool) -> List[PublicPlatform]:
        """Get all platforms

        :param bool `enabled`: List only enabled platforms

        :rtype List[:class:`<coingate.resources.public.Platform>`]

        Basic Usage::
          >>> client = CoinGate()
          >>> client.public.get_platforms()

        """
        response = self._client.request(
            "get", "v2/platforms", params={"enabled": enabled}
        ).json()

        return [PublicPlatform(**platform) for platform in response]
