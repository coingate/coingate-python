from ast import arg
from decimal import Decimal

import pytest
from coingate.exceptions import OrderIsNotValidException, OrderNotFoundException
from coingate.resources.order import Checkout, NewOrder, Order, PaginatedOrders

from .base_test_case import BaseTestCase


class TestOrderService(BaseTestCase):
    def test_create_without_optionals(self):
        order = self._create_test_order()

        assert isinstance(order, NewOrder)
        assert order.price_amount == Decimal("10")
        assert order.receive_currency == "EUR"
        assert order.price_currency == "EUR"

    @pytest.mark.parametrize(
        "callback_url,cancel_url,success_url,should_raise",
        [
            ("test-callback_url", "test-cancel_url", "test-success_url", True),
            (
                "https://coingate.com",
                "https://coingate.com",
                "https://coingate.com",
                False,
            ),
        ],
    )
    def test_create_with_optionals(
        self, callback_url: str, cancel_url: str, success_url: str, should_raise: bool
    ):
        def _create_order_with_optionals():
            return self._create_test_order(
                order_id="test-order_id",
                title="test-title",
                description="test-description",
                callback_url=callback_url,
                cancel_url=cancel_url,
                success_url=success_url,
                token="test-token",
                purchaser_email="test-purchaser_email@email.com",
            )

        if should_raise:
            with pytest.raises(OrderIsNotValidException) as exc_info:
                _create_order_with_optionals()

            expected_errors = [
                "Api order base success_url is not valid",
                "Api order base cancel_url is not valid",
                "Api order base callback_url is not valid",
            ]

            assert exc_info.value.message == "Order is not valid"
            assert len(exc_info.value.errors) == len(expected_errors)
            assert set(exc_info.value.errors) == set(expected_errors)
        else:
            order = _create_order_with_optionals()

            assert isinstance(order, NewOrder)
            assert order.price_amount == Decimal("10")
            assert order.receive_currency == "EUR"
            assert order.price_currency == "EUR"

    def test_checkout_without_valid_order(self):
        with pytest.raises(OrderNotFoundException) as exc_info:
            self.client.order.checkout(1, "EUR")

        assert exc_info.value.message == "Order does not exist"
        assert exc_info.value.errors is None

    @pytest.mark.parametrize(
        "pay_currency,should_raise",
        [("EUR", True), ("BTC", False), ("ETH", False), ("USD", True)],
    )
    def test_checkout_with_valid_order(self, pay_currency: str, should_raise: bool):
        order = self._create_test_order()

        def _create_checkout_with_valid_order():
            return self.client.order.checkout(order.id, pay_currency)

        if should_raise:
            with pytest.raises(OrderIsNotValidException) as exc_info:
                _create_checkout_with_valid_order()

            expected_errors = ["Pay currency is invalid"]

            assert exc_info.value.message == "Order is not valid"
            assert len(exc_info.value.errors) == len(expected_errors)
            assert set(exc_info.value.errors) == set(expected_errors)
        else:
            checkout = _create_checkout_with_valid_order()

            assert isinstance(checkout, Checkout)
            assert checkout.price_amount == order.price_amount
            assert checkout.receive_currency == "EUR"
            assert checkout.pay_currency == pay_currency
            assert checkout.platform is None

    def test_get_order_with_non_existing_order(self):
        with pytest.raises(OrderNotFoundException) as exc_info:
            self.client.order.get(1)

        assert exc_info.value.message == "Order not found"
        assert exc_info.value.errors is None

    def test_get_order_with_existing_order(self):
        order = self._create_test_order()
        fetched_order = self.client.order.get(order.id)

        assert isinstance(fetched_order, Order)
        assert fetched_order.id == order.id

    def test_get_all_orders_without_optionals(self):
        self._create_test_order()
        fetched_orders = self.client.order.get_all()

        self._assert_common_get_all_checks(fetched_orders)

    def test_get_all_orders_with_optionals(self):
        self._create_test_order()
        fetched_orders = self.client.order.get_all(per_page=1, page=1)

        self._assert_common_get_all_checks(fetched_orders)

        assert fetched_orders.per_page == 1
        assert fetched_orders.current_page == 1

    def _assert_common_get_all_checks(self, fetched_orders):
        assert isinstance(fetched_orders, PaginatedOrders)
        assert type(fetched_orders.orders) == list
        assert isinstance(fetched_orders.orders[0], Order)

    def _create_test_order(
        self,
        price_amount: Decimal = Decimal("10"),
        price_currency: str = "EUR",
        receive_currency: str = "EUR",
        **kwargs
    ):
        return self.client.order.create(
            price_amount, price_currency, receive_currency, **kwargs
        )
