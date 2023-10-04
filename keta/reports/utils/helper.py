import re
from rest_framework.exceptions import APIException


def format_date(date_str, ticket=None):
    pattern = r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})"
    match = re.search(pattern, date_str)
    if match:
        year, month, day = match.group("year", "month", "day")
        if year == "0001":
            raise APIException(
                f"There could not be generated the record as ticket {ticket} state is closed "
                f", however not resolution record was found"
            )
        return f"{day}/{month}/{year}"

    else:
        raise ValueError("Invalid date format")
