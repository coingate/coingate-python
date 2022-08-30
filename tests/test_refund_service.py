from decimal import Decimal

import pytest
from coingate.exceptions import (
    OrderNotFoundException,
    RefundIsNotValidException,
    RefundNotFoundException,
)
from coingate.resources.refund import (
    PaginatedRefunds,
    PaginatedRefundsRefund,
    Refund,
    RefundOrder,
)

from .base_test_case import BaseTestCase


class TestRefundService(BaseTestCase):
    def test_create_order_refund_wit_non_existing_order(self):
        with pytest.raises(OrderNotFoundException) as exc_info:
            self.client.refund.create_order_refund(
                1, Decimal("10"), "addy", 1, 1, "refund", "email@email.com", "id"
            )

        assert exc_info.value.message == "Order not found"
        assert exc_info.value.errors is None

    @pytest.mark.parametrize(
        "currency_id,platform_id,addy,should_raise",
        [(1, 6, "n47k2iuCNKMJxPndvRc3iGV3Td7NpWQhve", False), (1, 1, "addy", True)],
    )
    def test_create_order_refund_with_valid_order(
        self, currency_id: int, platform_id: int, addy: str, should_raise: bool
    ):
        if should_raise:
            with pytest.raises(RefundIsNotValidException) as exc_info:
                self._create_order_refund(addy, currency_id, platform_id)

            expected_errors = [
                "Crypto platform not found or does not belong to this currency"
            ]

            assert exc_info.value.message == "Refund is not valid"
            assert set(exc_info.value.errors) == set(expected_errors)
            assert len(exc_info.value.errors) == len(expected_errors)
        else:
            refund = self._create_order_refund(addy, currency_id, platform_id)

            assert isinstance(refund, Refund)
            assert refund.address == addy
            assert refund.order == RefundOrder(id=self.existing_big_order_id)

    def test_get_order_refund_with_non_existing_order(self):
        with pytest.raises(OrderNotFoundException) as exc_info:
            self.client.refund.get_order_refund(1, 1)

        assert exc_info.value.message == "Order not found"
        assert exc_info.value.errors is None

    @pytest.mark.parametrize("should_raise", [(True), (False)])
    def test_get_order_refund_with_existing_order(self, should_raise: bool):
        if should_raise:
            with pytest.raises(RefundNotFoundException) as exc_info:
                self.client.refund.get_order_refund(self.existing_big_order_id, 0)

            assert exc_info.value.message == "Refund not found"
            assert exc_info.value.errors is None
        else:
            refund = self._create_order_refund()
            fetched_refund = self.client.refund.get_order_refund(
                self.existing_big_order_id, refund.id
            )

            assert isinstance(fetched_refund, Refund)
            assert fetched_refund.order == RefundOrder(id=self.existing_big_order_id)

    def test_get_order_refunds(self):
        refunds = self.client.refund.get_order_refunds(self.existing_big_order_id)

        self._assert_common_refund_checks(refunds)

    def test_get_refunds(self):
        refunds = self.client.refund.get_refunds()

        self._assert_common_refund_checks(refunds)

    def _create_order_refund(
        self,
        addy: str = "n47k2iuCNKMJxPndvRc3iGV3Td7NpWQhve",
        currency_id: int = 1,
        platform_id: int = 6,
    ):
        return self.client.refund.create_order_refund(
            self.existing_big_order_id,
            Decimal("1"),
            addy,
            currency_id,
            platform_id,
            "reason",
            "email@email.com",
            "01GBPW7M2G5XQK3BE50XQRA36E",
        )

    def _assert_common_refund_checks(self, refunds):
        assert isinstance(refunds, PaginatedRefunds)
        assert refunds.current_page == 1
        assert refunds.per_page == 100
        assert type(refunds.total_refunds) == int
        assert type(refunds.total_pages) == int
        assert isinstance(refunds.refunds[0], PaginatedRefundsRefund)
