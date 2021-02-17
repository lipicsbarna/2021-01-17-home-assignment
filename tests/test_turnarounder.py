from datetime import datetime
import pytest
from due_date_calculator.turnarounder import add_turnaround
from due_date_calculator.turnarounder import TurnaroundTimeError


manual_start = datetime(2018,4,23,9,11,0)

add_turnaround_cases = [
    ("2 days", datetime(2018, 4, 25, 9, 11)),
    ("2 hours", datetime(2018,4,23,11,11,0)),
    ("9 hours", datetime(2018,4,24,10,11,0)),
    ("16 hours", datetime(2018,4,25,9,11,0))
]

@pytest.mark.parametrize("turnaround, expected", add_turnaround_cases)
def test_add_turnaround(turnaround, expected):
    assert add_turnaround(manual_start, turnaround) == expected


wrong_input_cases = [
    ("-2 days", ValueError),
    ("something_weird", TurnaroundTimeError),
    ("two days", TurnaroundTimeError),

]
@pytest.mark.parametrize("wrong_input, exception", wrong_input_cases)
def test_add_wrong_inputs(wrong_input, exception):
    with pytest.raises(exception):
        add_turnaround(manual_start, wrong_input)