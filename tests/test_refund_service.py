from decimal import Decimal

import pytest
from coingate.exceptions import OrderNotFoundException

from .base_test_case import BaseTestCase


class TestRefundService(BaseTestCase):
    def test_create_order_refund_wit_non_existing_order(self):
        with pytest.raises(OrderNotFoundException) as exc_info:
            self.client.refund.create_order_refund(
                1, Decimal("10"), "addy", 1, 1, "refund", "email@email.com", "id"
            )

        assert exc_info.value.message == "Order not found"
        assert exc_info.value.errors is None
