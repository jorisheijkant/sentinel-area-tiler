import re
from datetime import date, timedelta

_DATE_FORMAT_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")

def _is_valid_date_format(value: str) -> bool:
    return bool(_DATE_FORMAT_PATTERN.match(value))

def get_dates(start_date: str, end_date: str) -> list[date]:
    if not _is_valid_date_format(start_date):
        raise ValueError(f"start_date '{start_date}' must be in YYYY-MM-DD format")
    if not _is_valid_date_format(end_date):
        raise ValueError(f"end_date '{end_date}' must be in YYYY-MM-DD format")

    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)

    if start > end:
        raise ValueError(f"start_date {start_date} must be before end_date {end_date}")

    days = (end - start).days
    return [start + timedelta(days=i) for i in range(days + 1)]

