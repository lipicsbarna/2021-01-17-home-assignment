from datetime import datetime

from due_date_calculator.dateparser import parse_datetime
from due_date_calculator.turnarounder import add_turnaround


def CalculateDueDate(turnaround: str, start_date_time: str = None, start_date_time_format: str = None):
    if start_date_time is None:
        start = parse_datetime()
    elif start_date_time_format is None:
        start = parse_datetime(start_date_time)
    else:
        start = parse_datetime(start_date_time, start_date_time_format)

    return datetime.strftime(add_turnaround(start, turnaround), "%Y-%m-%d %H:%M")