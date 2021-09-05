from datetime import timedelta
from workdays import (RobotWorkDay, RobotWorkHalfDay,
	RobotShiftStartDay, RobotShiftEndDay, convert_to_datetime
)
import json

def load_json(json_obj):
	"""
	Loads json data from json files.	
	"""
	data = json.load(json_obj)
	return data


def parse_roboRate_values(roboRate, day):
	"""
	Parse the necessary values from roboRate.

	Parameters
	----------
	roboRate : dict
		The rates as determined by input.
	day : int
		Represents day of the week. 0 for Monday and 6 for Sunday.

	Returns
	-------
	day_start : str
		Start of a standard/extra day, equivalent to end of a standard/extra night.
	day_end : str
		End of a standard/extra day, equivalent to start of a standard/extra night.
	day_rate : int
		Minutely rate of a standard/extra day.
	night_rate : int
		Minutely rate of a standard/extra night.
	"""
	# parse extra fees if weekend
	if day > 4:
		weekend_day = roboRate.get("extraDay")
		weekend_night = roboRate.get("extraNight")

		day_start = weekend_day.get("start")
		day_end = weekend_day.get("end")
		day_rate = weekend_day.get("value")
		night_rate = weekend_night.get("value")
	# parse standard fees if weekday
	else:
		weekday_day = roboRate.get("standardDay")
		weekday_night = roboRate.get("standardNight")

		day_start = weekday_day.get("start")
		day_end = weekday_day.get("end")
		day_rate = weekday_day.get("value")
		night_rate = weekday_night.get("value")

	return day_start, day_end, int(day_rate), int(night_rate)

def calculate_half_day_pay(shift_start, shift_end, roboRate):
	"""
	Calculate value of robot's work for the half-day.

	Parameters
	----------
	shift_start : datetime object instance
		str in "HH:MM:SS" that is converted to datetime object using `datetime.strptime()`
		represents the start of the shift.
	shift_end : datetime object instance
		str in "HH:MM:SS" that is converted to datetime object using `datetime.strptime()`
		represents the end of the shift.
	roboRate : dict
		The rates as determined by input.

	Returns
	-------
	value : int
		Value of robot's work for the half-day.
	"""
	day = shift_start.weekday()
		
	# parse and assign various values
	values = parse_roboRate_values(roboRate, day)
	day_start = values[0]
	day_end = values[1]
	day_rate = values[2]
	night_rate = values[3]

	# generate half-day instance
	work_day = RobotWorkHalfDay( shift_start, shift_end,
			day_start, day_end, day_rate, night_rate)
	
	# get minutes worked for the day
	minutes_worked = work_day.get_minutes_worked(
			work_day.get_break_timings())
	
	# adds value calculated to the total
	value = work_day.calculate_pay(
			minutes_worked['day_minutes'], minutes_worked['night_minutes'])
	
	return int(value)


def calculate_total_pay(shift_start, shift_end, roboRate):
	"""
	Calculate value of robot's work for the duration of the multi-day shift.

	Parameters
	----------
	shift_start : datetime object instance
		str in "HH:MM:SS" that is converted to datetime object using `datetime.strptime()`
		represents the start of the shift.
	shift_end : datetime object instance
		str in "HH:MM:SS" that is converted to datetime object using `datetime.strptime()`
		represents the end of the shift.
	roboRate : dict
		The rates as determined by input.

	Returns
	-------
	value : int
		Value of robot's work for the half-day.
	"""
	value = 0
	current_day = shift_start

	time_of_last_break = shift_start.strftime("%H%M")

	# Comparing dates of the same day same month & different year 
	# results in 0 days for some methods but not others.
	# Comparing  dates of the same day same year & different month
	# results in 0 days for some methods but not others, which is
	# inconsistent with the dates of same day & month but different year.
	
	# This issue is resolved by taking the highest number calculated by
	# using the various methods
	
	# Method 1 of comparing dates:
	# Using numerical difference in days
	shift_start_day = int(shift_start.strftime("%d"))
	shift_end_day = int(shift_end.strftime("%d"))
	shift_duration_days = (shift_end_day - shift_start_day)

	# Method 2 of comparing dates:
	# Using timedelta.days to get difference in days
	duration_days = (shift_end - shift_start).days
	if duration_days > shift_duration_days:
		shift_duration_days = duration_days
		
	# Method 3 of comparing dates:
	# Using timedelta.days to get difference in seconds then converting to days
	shift_duration_seconds = (shift_end - shift_start).seconds
	duration_days = int(shift_duration_seconds / 86400) \
			+ (shift_duration_seconds % 86400 > 0)
	if duration_days > shift_duration_days:
		shift_duration_days = duration_days

	# loops through all the days in the shift
	for i in range(shift_duration_days + 1):
		# Return the day of the week as an integer, where Monday is 0 and Sunday is 6.
		day = current_day.weekday()
		current_day += timedelta(days=1)

		# parse and assign various values
		values = parse_roboRate_values(roboRate, day)
		day_start = values[0]
		day_end = values[1]
		day_rate = values[2]
		night_rate = values[3]
		
		# start the shift
		if i == 0:
			work_day = RobotShiftStartDay(shift_start,
					day_start, day_end, day_rate, night_rate)
		# end the shift
		elif i == shift_duration_days:
			work_day = RobotShiftEndDay(shift_end, day_start, day_end,
					day_rate, night_rate, time_of_last_break)
		# during the shift
		else: 
			work_day = RobotWorkDay(day_start, day_end, 
					day_rate, night_rate, time_of_last_break)
		
		# get minutes worked for the day
		minutes_worked = work_day.get_minutes_worked(
				work_day.get_break_timings())
		
		# set the time of the last break taken for next day
		for break_time in work_day.get_break_timings():
			time_of_last_break = break_time.strftime("%H%M")
		
		# adds value calculated to the total
		value += work_day.calculate_pay(
				minutes_worked['day_minutes'], minutes_worked['night_minutes'])

	return int(value)


def main():
	"""
	Generate expected value with the given JSON object.

	Returns
	-------
	expected_value : int
		The expected value of the robot given the shift period.`
	"""
	json_file = open(INPUT_FILE, encoding="utf8")
	data = load_json(json_file)
	
	shift = data.get("shift")
	roboRate = data.get("roboRate")

	shift_start = convert_to_datetime(shift.get("start"))
	shift_end = convert_to_datetime(shift.get("end"))
	
	# if shift starts and ends on the same day, calculate pay with half-day
	if shift_start.strftime("%Y%m%d") == shift_end.strftime("%Y%m%d"):
		value = calculate_half_day_pay(shift_start, shift_end, roboRate)

	else:
		value = calculate_total_pay(shift_start, shift_end, roboRate)

	return {"value": value}


if __name__ == '__main__':
	WORK_DURATION_IN_HOURS = 8
	BREAK_DURATION_IN_HOURS = 1
	INPUT_FILE = "input.json"
	
	value = main()
	print(value)