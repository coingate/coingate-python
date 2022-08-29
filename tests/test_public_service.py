from datetime import datetime
from decimal import Decimal
from typing import Optional, Union

import pytest
from coingate.resources.public import (Currency, ExchangesRates,
                                       ExchangeTrader, Ping, Platform)
from typing_extensions import Literal

from tests.base_test_case import BaseTestCase


class TestPublicService(BaseTestCase):
    @pytest.mark.parametrize(
        "from_currency,to_currency,expectedType",
        [("ETH", "EUR", Decimal), ("EUR", "BTC", Decimal), ("NAN", "NAN", None)],
    )
    def test_get_exchange_rate_for_merchant(
        self, from_currency: str, to_currency: str, expectedType: Optional[Decimal]
    ):
        rate = self.client.public.get_exchange_rate_for_merchant(
            from_currency, to_currency
        )

        if expectedType is not None:
            assert type(rate) is expectedType
        else:
            assert rate is expectedType

    @pytest.mark.parametrize(
        "kind,from_currency,to_currency,expectedType",
        [
            ("buy", "ETH", "EUR", Decimal),
            ("sell", "BTC", "EUR", Decimal),
            ("sell", "NAN", "NAN", None),
        ],
    )
    def test_get_exchange_rate_for_trader(
        self,
        kind: Literal["buy", "sell"],
        from_currency: str,
        to_currency: str,
        expectedType: Optional[Decimal],
    ):
        rate = self.client.public.get_exchange_rate_for_trader(
            kind, from_currency, to_currency
        )

        if expectedType is not None:
            assert type(rate) is expectedType
        else:
            assert rate is expectedType

    def test_get_all_exchange_rates(self):
        rates = self.client.public.get_all_exchange_rates()

        assert isinstance(rates, ExchangesRates)
        assert isinstance(rates.merchant, dict)
        assert isinstance(rates.trader, ExchangeTrader)
        assert isinstance(rates.trader.buy, dict)
        assert isinstance(rates.trader.sell, dict)

    def test_get_merchant_exchange_rates(self):
        rates = self.client.public.get_merchant_exchange_rates()

        assert rates is not None

    @pytest.mark.parametrize(
        "kind,expectedType",
        [
            ("sell", dict),
            ("buy", dict),
            (None, ExchangeTrader),
        ],
    )
    def test_get_trader_exchange_rates(
        self,
        kind: Optional[Literal["buy", "sell"]],
        expectedType: Union[dict, ExchangeTrader],
    ):
        rates = self.client.public.get_trader_exchange_rates(kind)

        assert type(rates) == expectedType

    def test_ping(self):
        answer = self.client.public.ping()

        assert isinstance(answer, Ping)
        assert answer.ping == "pong"
        assert type(answer.time) == datetime

    @pytest.mark.parametrize("separator", [(None), ("|")])
    def test_get_ip_addresses(self, separator: Optional[str]):
        answer = self.client.public.get_ip_addresses(separator)

        assert type(answer) == str

        if separator is not None:
            ip_addresses = answer.split(separator)
            assert len(ip_addresses) != 0

    @pytest.mark.parametrize(
        "native,enabled,merchant_pay,merchant_receive,kind",
        [
            (True, True, True, True, "crypto"),
            (True, True, True, True, "fiat"),
            (False, False, False, False, "crypto"),
            (False, False, False, False, "fiat"),
            (True, False, True, False, "crypto"),
            (True, False, True, False, "fiat"),
        ],
    )
    def test_get_currencies(
        self,
        native: bool,
        enabled: bool,
        merchant_pay: bool,
        merchant_receive: bool,
        kind: Literal["crypto", "fiat"],
    ):
        currencies = self.client.public.get_currencies(
            native, enabled, merchant_pay, merchant_receive, kind
        )

        if kind == "crypto":
            assert len(currencies) != 0
            assert isinstance(currencies[0], Currency)
        else:
            assert len(currencies) == 0

    @pytest.mark.parametrize("enabled", [(True), (False)])
    def test_get_platforms(self, enabled: bool):
        platforms = self.client.public.get_platforms(enabled)

        assert len(platforms) != 0
        assert isinstance(platforms[0], Platform)
