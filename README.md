# 2021-01-17-home-assignment

## Usage:
`>>from due_date_calculator import CalculateDueDate`


if only turnaround_time is given, we calculate due date from now

assuming that now is '2021-02-17 11:37'

`>> CalculateDueDate("2 days")` 

`Returns '2021-02-19 11:37'`

or

`>> CalculateDueDate("16 hours")`

`Returns '2021-02-19 11:37'`

***
We can specify a start_date_time, it recognises three common formats (according to my experience):

* "%Y-%m-%d %H:%M"
* "%Y%m%d%H%M"
* "%Y/%m/%d %H:%M"
        

`>> CalculateDueDate(turnaround="2 days", start_date_time="2020-01-16 9:00")`

`Returns '2020-01-18 09:00'`

or

`>> CalculateDueDate(turnaround="5 hours", start_date_time="2020/01/16 9:00")`

`Returns '2020-01-18 14:00'`

***
You also can specify your custom date format:

`>> CalculateDueDate(turnaround="2 days", start_date_time="2020_01_16-09_00", start_date_time_format="%Y_%m_%d-%H_%M")`

`Returns '2020-01-18 09:00'`



