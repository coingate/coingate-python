from decimal import Decimal

import pytest
from coingate.exceptions import LedgerAccountNotFoundException
from coingate.resources.ledger import (
    LedgerAccount,
    LedgerAccountCurrency,
    PaginatedLedgerAccounts,
)

from .base_test_case import BaseTestCase


class TestLedgerService(BaseTestCase):
    @pytest.mark.parametrize(
        "id,should_raise", [("01GBPW7M2G5XQK3BE50XQRA36E", False), ("id", True)]
    )
    def test_get(self, id: str, should_raise: bool):
        if should_raise:
            with pytest.raises(LedgerAccountNotFoundException) as exc_info:
                self.client.ledger.get(id)

            assert exc_info.value.message == "Ledger Account not found"
            assert exc_info.value.errors is None

            return

        account = self.client.ledger.get(id)

        assert isinstance(account, LedgerAccount)
        assert isinstance(account.id, str)
        assert isinstance(account.balance, Decimal)
        assert isinstance(account.status, str)

        currency = account.currency

        assert isinstance(currency, LedgerAccountCurrency)
        assert isinstance(currency.id, int)
        assert isinstance(currency.title, str)
        assert isinstance(currency.symbol, str)

    def test_get_all(self):
        response = self.client.ledger.get_all()

        assert isinstance(response, PaginatedLedgerAccounts)
        assert isinstance(response.current_page, int)
        assert isinstance(response.per_page, int)
        assert isinstance(response.total_accounts, int)
        assert isinstance(response.total_pages, int)
        assert isinstance(response.accounts[0], LedgerAccount)
