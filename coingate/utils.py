from datetime import datetime
from typing import Optional


def date_to_str_or_none(date: Optional[datetime]) -> Optional[str]:
    if date is not None:
        return date.strftime("%Y-%m-%d")

    return None
