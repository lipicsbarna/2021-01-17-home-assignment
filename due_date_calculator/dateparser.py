from multipledispatch import dispatch
from datetime import datetime


@dispatch(str, str)
def parse_datetime(date_time: str, date_time_format: str) -> datetime:
    try:
        return datetime.strptime(date_time, date_time_format)
    except ValueError:
        raise


@dispatch(str)
def parse_datetime(date_time: str) -> datetime:
    common_formats = [
        "%Y-%m-%d %H:%M",
        "%Y%m%d%H%M",
        "%Y/%m/%d %H:%M"
    ]

    for format_ in common_formats:
        try:
            return_datetime = datetime.strptime(date_time, format_)
            break
        except:
            continue

    try:
        return return_datetime
    except:
        raise ValueError("""
            Not appropriate format. 
            Try providing your custom format in parameter.
            Example:
            >> CalculateDueDate(..., ..., date_time_format="%Y_%M_%d_%H_%m")""")

@dispatch()
def parse_datetime() -> datetime:
    now = datetime.strftime(datetime.today(), "%Y-%m-%d %H:%M")
    return parse_datetime(now)