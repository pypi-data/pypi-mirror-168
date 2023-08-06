"""Functionality related to asking the user for IAM binding timeframes."""
from typing import List
from typing import cast

import pendulum
import questionary as q
from pydantic import BaseModel


class Expiry(BaseModel):
    """An `Expiry` denotes a timeframe associated with an IAM binding.

    Attributes:
        name: Friendly name of the timeframe, such as "Until end of today`
        timestamp: ISO8601 timestamp
    """

    name: str
    timestamp: str


def ask_for_expiry() -> Expiry:
    """Prompt the user to select a timeframe constraint to be associated with the IAM bindings.

    Returns:
        An user selected `Expiry` to be associated with the IAM bindings.
    """
    answer = q.select(
        message="For how long?",
        qmark="📅",
        choices=[q.Choice(item.name, value=item) for item in _expiry_timestamp_items()],
    ).ask()
    return cast(Expiry, answer)


def _expiry_timestamp_items() -> List[Expiry]:
    """Return a list of suggested expiry timestamps that can be selected by the user.

    Returns:
        List of timestamps used for specifying auth expiry times

    """
    return [
        Expiry(name="Until end of today", timestamp=timestamp_at(end_of="day")),
        Expiry(name="Until end of tomorrow", timestamp=timestamp_at(end_of="day", days=1)),
        Expiry(name="Until end of current week", timestamp=timestamp_at(end_of="week")),
        Expiry(name="Until end of current month", timestamp=timestamp_at(end_of="month")),
        Expiry(name="Until end of current year", timestamp=timestamp_at(end_of="year")),
        Expiry(name="2 hours", timestamp=timestamp_at(hours=2)),
        Expiry(name="4 hours", timestamp=timestamp_at(hours=4)),
        Expiry(name="1 week", timestamp=timestamp_at(end_of="day", days=7)),
        Expiry(name="2 weeks", timestamp=timestamp_at(end_of="day", weeks=2)),
        Expiry(name="Forever [forevah evah]", timestamp=timestamp_at(end_of="century")),
    ]


def timestamp_at(end_of: str = "", **offset: int) -> str:
    """Generate a UTC ISO8601 string relative to the current timestamp.

    The resulting timestamp can be further specified by supplying additional Pendulum offsets and `end_of` parameters.

    Examples:
        `hours=2` means the timestamp from now + 2 hours
        `days=4` and `end_of="day"` means the timestamp from now + 4 days, at the end of that day (23:59:59)

    Args:
        end_of: Could be any of Pendulum's `end_of` parameters
        **offset: Could be any of Pendulum's parameters

    Returns:
        ISO8601 UTC string
    """
    timestamp = pendulum.now("UTC")
    if offset:
        timestamp = timestamp.add(**offset)
    if end_of:
        timestamp = timestamp.end_of(end_of)

    timestamp_str = str(timestamp.to_iso8601_string())
    if len(timestamp_str) > 25:
        # Remove microseconds and milliseconds
        timestamp_str = timestamp_str[:19] + timestamp_str[26:]
    return timestamp_str
