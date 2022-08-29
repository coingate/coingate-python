from datetime import datetime
from typing import Optional

import pytest
from coingate.utils import date_to_str_or_none


class TestUtils:
    @pytest.mark.parametrize(
        "date,expectedType", [(datetime(2022, 10, 10, 10, 12, 11), str), (None, None)]
    )
    def test_date_to_str_or_none(
        self, date: Optional[datetime], expectedType: Optional[str]
    ):
        value = date_to_str_or_none(date)

        if expectedType is not None:
            assert type(value) == expectedType
        else:
            assert value is None
