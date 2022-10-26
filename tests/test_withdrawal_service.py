from datetime import datetime
from decimal import Decimal

import pytest
from coingate.exceptions import WithdrawalNotFoundException
from coingate.resources.currency import Currency
from coingate.resources.withdrawal import (
    PaginatedWithdrawals,
    PayoutSetting,
    Withdrawal,
)

from .base_test_case import BaseTestCase


class TestWithdrawalService(BaseTestCase):
    @pytest.mark.parametrize("id,should_raise", [(14, False), (1, True)])
    def test_get(self, id: int, should_raise: bool):
        if should_raise:
            with pytest.raises(WithdrawalNotFoundException) as exc_info:
                self.client.withdrawal.get(id)

            assert exc_info.value.message == "Withdrawal does not exist"
            assert exc_info.value.errors is None

            return

        withdrawal = self.client.withdrawal.get(id)
        self._assert_common_withdrawal_checks(withdrawal)

    def test_get_all(self):
        response = self.client.withdrawal.get_all()

        assert isinstance(response, PaginatedWithdrawals)
        assert isinstance(response.current_page, int)
        assert isinstance(response.per_page, int)
        assert isinstance(response.total_withdrawals, int)
        assert isinstance(response.total_pages, int)

        withdrawal = response.withdrawals[0]
        self._assert_common_withdrawal_checks(withdrawal)

    def _assert_common_withdrawal_checks(self, withdrawal: Withdrawal):
        assert isinstance(withdrawal, Withdrawal)
        assert isinstance(withdrawal.id, int)
        assert isinstance(withdrawal.status, str)
        assert isinstance(withdrawal.amount, Decimal)
        assert isinstance(withdrawal.created_at, datetime)
        assert isinstance(withdrawal.currency, Currency)
        assert isinstance(withdrawal.payout_setting, PayoutSetting)
