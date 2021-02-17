from datetime import datetime
import pytest
from freezegun import freeze_time
from due_date_calculator.dateparser import parse_datetime



@freeze_time("2020-01-16 19:00:00")
def test_parse_datetime_no_param():
    # No params mean now
    assert parse_datetime() == datetime(2020, 1, 16, 19, 0, 0)


expected = [datetime.strptime("2020-01-16 19:00", "%Y-%m-%d %H:%M")]
dates_to_parse = [
    "2020-01-16 19:00",
    "202001161900",
    "2020/01/16 19:00"
]
test_cases_common_formats = list(zip(dates_to_parse, expected*len(dates_to_parse)))

@pytest.mark.parametrize("input_datetime, expected", test_cases_common_formats)
def test_parse_datetime_common_format(input_datetime, expected):
    assert parse_datetime(input_datetime) == expected


def test_wrong_common_format():
    # Invalid
    with pytest.raises(ValueError):
        parse_datetime('something_weird')


def test_parse_datetime_explicit_format():
    # Given format
    assert parse_datetime(
        "2020-01-16 19:00",
        "%Y-%m-%d %H:%M") == datetime.strptime("2020-01-16 19:00", "%Y-%m-%d %H:%M")

    with pytest.raises(ValueError):
        parse_datetime("2020-01-16 19:00", "%Y%m%d%H%M")