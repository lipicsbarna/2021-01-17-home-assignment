from datetime import datetime, timedelta
from multipledispatch import dispatch

from due_date_calculator.config import work_start_hour, work_end_hour, working_hours


class TurnaroundTimeError(Exception):
    def __init__(self):
        self.message = """
        You need to specify the turnaround time with the following schema:
        <number> days/hours, e.g.:
        >> CalculateDueDate(turnaround="2 days")
        or
        >> CalculateDueDate(turnaround="13 hours")
        """
        super().__init__(self.message)


# Won't be used by user, calculates the whole day difference
@dispatch(datetime, int)
def add_turnaround(start: datetime, turnaround_days: int):
    assert work_start_hour <= start.hour < work_end_hour, \
        f"The time of submission has to be in working hours: {work_start_hour} - {work_end_hour}"
    weekdays = [0, 1, 2, 3, 4]

    current_date = start
    days_left = turnaround_days
    while days_left > 0:
        if current_date.weekday() in weekdays:
            current_date += timedelta(days=1)
            days_left -= 1
        else:
            current_date += timedelta(days=1)

    return current_date


# Won't be used by user; if turnaround was given in hours, this will be used.
@dispatch(datetime, int, bool)
def add_turnaround(start: datetime, turnaround: int, in_hours: bool = True) -> datetime:
    assert work_start_hour <= start.hour < work_end_hour, \
        f"The time of submission has to be in working hours: {work_start_hour} - {work_end_hour}"

    end_of_start_day = datetime(start.year, start.month, start.day, work_end_hour, 0)

    # If we can stay intraday
    if start + timedelta(hours=turnaround) < end_of_start_day:
        return_turnaround_datetime = start + timedelta(hours=turnaround)

    elif (start.hour + turnaround % working_hours) < work_end_hour and turnaround > working_hours:
        whole_days_added = add_turnaround(start, turnaround // working_hours)
        return_turnaround_datetime = whole_days_added + timedelta(hours=(turnaround % working_hours))

    else:
        remains_today_seconds = (end_of_start_day - start).seconds
        whole_days = turnaround // working_hours

        partial_seconds_remained = turnaround * 3600 - whole_days * working_hours * 3600 - remains_today_seconds

        tomorrow_date = start + timedelta(days=1)
        tomorrow_morning = datetime(tomorrow_date.year, tomorrow_date.month, tomorrow_date.day, work_start_hour, 0)

        whole_days_added = add_turnaround(tomorrow_morning, whole_days)
        return_turnaround_datetime = whole_days_added + timedelta(seconds=partial_seconds_remained)

    return return_turnaround_datetime


# This will be called from CalculateDueDate
@dispatch(datetime, str)
def add_turnaround(start: datetime, turnaround: str) -> datetime:
    split_turnaround = turnaround.split(' ')
    if len(split_turnaround) == 2:
        pass
    else:
        raise TurnaroundTimeError

    try:
        turnaround_number = int(split_turnaround[0])
    except:
        raise TurnaroundTimeError

    if turnaround_number < 0:
        raise ValueError("Must set a positive number to turnaround time, e.g. '2 days' ")

    turnaround_timerange = (split_turnaround[1]).lower()

    if not all([True if char.isalpha() else False for char in list(turnaround_timerange) ]):
        raise TurnaroundTimeError

    if turnaround_timerange == 'days':
        return_turnaround = add_turnaround(start, turnaround_number)
    elif turnaround_timerange == 'hours':
        return_turnaround = add_turnaround(start, turnaround_number, True)
    else:
        raise TurnaroundTimeError

    return return_turnaround

