# Robot Salary Calculator

This is a simple calculator that takes a json input and outputs the total value as described in the problem statement. This project mainly focuses on the utilisation of the python `datetime` module to calculate the working time clocked by the Robot.


## Problem Statement

### CodeIT Suisse Entry Challenge
It is the year 2038 and robots have the right to get paid for the work they do. As an employer of robots, you need to calculate how much a robot gets paid for cleaning your apartment.

How much a robot gets paid depends on when you ask the robot to work. After all, during the day the robot can be a little louder and work a bit faster whilst everyone is out of the house, but at night, you will need to turn on the super quiet mode, which takes more effort! Robots also cost a bit more over weekends, due to higher demand.

Your robot rates calculator needs to consider the following:
- A standard minutely rate for weekdays, and an ‘extra’ rate for weekends.
- When rates switches between day and night rates, for a total of four different rates (weekday/weekend + day/night).
- For every eight hours, the robot needs to take an hour of unpaid break (or part thereof) for planned system maintenance.

### Features

- Calculate pay based on work shift of Robot.
- Accommodates partial day's work, up to an unlimited number of work days.
- Differentiate weekdays & weekends with different daily rates.
- Differentiate day & night with different minutely rates.
- Robot takes 1 hour break for every 8 hours of work, which is accounted for.

### Assumptions

- There are 24 hours a day, 7 days a week and 2 weekends and 5 weekdays in a week.
- Leap year occurs every 4 years and skips every 4 centuries.
- Start of shift given always occurs before end of shift.
- Start of the day is always after 00:00:00 and before end of the day, which is always before 23:59:59 of the same day.

<!-- GETTING STARTED -->
## Getting Started

This project is the submission for the above coding challenge.

### Prerequisites

Python3.8 is recommended for this version. Check the full installation guide <a href="https://docs.python.org/3/using/windows.html">here</a>.
  
### Installation

1. Clone the repo
   ```bash
   git clone https://github.com/DavidLHW/robot-salary-calculator.git
   ```

2. Update `input.json` with relevant input information. See <a href="#examples">Examples</a>.

3. Run `main.py`
   ```sh
   python3 ./main.py
   ```

<!-- EXAMPLES -->
## Examples

Sample input:
```json
{
	"shift": {
		"start": "2038-01-01T20:15:00",
		"end": "2038-01-02T04:15:00"
	},
	"roboRate": {
		"standardDay": {
			"start": "07:00:00",
			"end": "23:00:00",
			"value": 20
		},
		"standardNight": {
			"start": "23:00:00",
			"end": "07:00:00",
			"value": 25
		},
		"extraDay": {
			"start": "07:00:00",
			"end": "23:00:00",
			"value": 30
		},
		"extraNight": {
			"start": "23:00:00",
			"end": "07:00:00",
			"value": 35
		}
	}
}
```


Sample output:
```json
{ "value": 13725 }
```
