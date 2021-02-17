from freezegun import freeze_time
from datetime import datetime
from itertools import combinations
import pytest

from due_date_calculator.duedatecalculator import CalculateDueDate
from due_date_calculator.turnarounder import TurnaroundTimeError


only_turnaround_given = [
    ("2 days", "2020-01-18 15:23"),
    ("0 days", "2020-01-16 15:23"),
    ("1 hours", "2020-01-16 16:23"),
    ("3 hours", "2020-01-17 10:23"),
    ("17 hours", "2020-01-18 16:23"),
    ("26 hours", "2020-01-22 09:23")
]


@freeze_time("2020-01-16 15:23:00")
@pytest.mark.parametrize("param_turnaround, expected", only_turnaround_given)
def test_calculate_duedate_without_explicit_datetime(param_turnaround, expected):
    assert CalculateDueDate(param_turnaround) == expected

#####################

exceptions = [
    ("-1 days", ValueError),
    ("two days", TurnaroundTimeError),
    ("something weird", TurnaroundTimeError),
    ("2020 11", TurnaroundTimeError),
    ("110 weeks", TurnaroundTimeError)
]


@pytest.mark.parametrize("param, exception", exceptions)
def test_exceptions(param, exception):
    with pytest.raises(exception):
        CalculateDueDate(param)

#####################

turnarounds = ["2 days", "3 hours", "0 days", "0 hours", "17 hours", "26 hours"]
expected = ["2018-04-25 09:11", "2018-04-23 12:11", "2018-04-23 09:11", "2018-04-23 09:11", "2018-04-25 10:11",
            "2018-04-26 11:11"]
turnarounds_with_expected = list(zip(turnarounds, expected))

common_formats = [
    "%Y-%m-%d %H:%M",
    "%Y%m%d%H%M",
    "%Y/%m/%d %H:%M"
]

manual_start = datetime(2018, 4, 23, 9, 11)
manual_dates_with_formats = [datetime.strftime(manual_start, format_) for format_ in common_formats]

dates_and_turnarounds = manual_dates_with_formats + turnarounds_with_expected
_all_format_variations = [
    comb for comb in list(combinations(dates_and_turnarounds, 2))
    if type(comb[1]) == tuple and
       type(comb[0]) == str]

all_format_variations = list((vari[0], vari[1][0], vari[1][1]) for vari in _all_format_variations)


@pytest.mark.parametrize("start_date, turnaround, expected", all_format_variations)
def test_calculate_duedate_with_common_dateformats(start_date, turnaround, expected):
    assert CalculateDueDate(turnaround=turnaround, start_date_time=start_date) == expected

#####################

all_manual_explicit_formats = [(format_, datetime.strftime(manual_start, format_)) for format_ in common_formats]
explicit_dates_and_turnarounds = all_manual_explicit_formats + turnarounds_with_expected
_all_explicit_format_variations = [
    comb for comb in list(combinations(explicit_dates_and_turnarounds, 2))
    if type(comb[1]) == tuple and type(comb[0]) == str]

all_explicit_format_variations = [
    vari for vari in list(combinations(explicit_dates_and_turnarounds, 2))
    if
    not (vari[0][0][0]).isdigit() and
    (vari[1][0][0]).isdigit()
]
flattened_explicit_variations = [
    (tup[0][0], tup[0][1], tup[1][0], tup[1][1]) for tup in all_explicit_format_variations
]


@pytest.mark.parametrize("format_, start_date, turnaround, expected", flattened_explicit_variations)
def test_calculate_duedate_explicit_dateformat(format_, start_date, turnaround, expected):
    assert CalculateDueDate(turnaround=turnaround, start_date_time=start_date,
                            start_date_time_format=format_) == expected

#####################

wrong_formats = [
    ('1hours', '2019-11111-2', '%Y%m%d'),
    ('1hours', "2121212121", "something weird"),
    ('1hours', "2019-01-01 01:01", "%Y%m%d %H%m")
]


@pytest.mark.parametrize("turnaround, start_date, format_", wrong_formats)
def test_exceptions_with_format(turnaround, start_date, format_):
    with pytest.raises(Exception):
        CalculateDueDate(turnaround=turnaround, start_date_time=start_date, start_date_time_format=format_)
