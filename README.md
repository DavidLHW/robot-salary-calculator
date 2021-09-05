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

<!-- GETTING STARTED -->
## Getting Started

This project is the submission for the above coding challenge.

### Prerequisites

Python3.8 is recommended for this version. Check the full installation guide <a href="https://docs.python.org/3/using/windows.html">here</a>.
  
### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/DavidLHW/robot-salary-calculator.git
   ```
   
2. Update `input.json` with relevant input information. See <a href="#examples">Examples</a>.

4. Run `main.py`
   ```
   python3 ./main.py
   ```

<!-- EXAMPLES -->
## Examples

Sample input:
```
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
```
{ "value": 13725 }
```
