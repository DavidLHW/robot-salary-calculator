from main import RobotWorkDay, RobotShiftStartDay, RobotShiftEndDay, RobotWorkHalfDay
from datetime import datetime

def get_work_cycle(work_duration_in_hours, break_duration_in_hours):
	""" 
	Generate robot's work cycle based on the given `work_duration_in_hours`
	and `break_duration_in_hours`.
	
	`work_break_period` is the period of
	days that `break_timings` will repeat for an assumed infinte shift
	duration.
	
	`work_cycle_in_days` is the period of days that will repeat
	for an assumed infinite shift duration.
	
	Parameters
	----------
	work_duration_in_hours : int
		The robot's work duration in hours.
	break_duration_in_hours : int
		The robot's break duration in hours.
	
	Returns
	-------
	work_cycle_in_days : int
		The robot's work cycle in number of days.

	Example
	-------
	If the robot has a 8 hour work duration and 1 hour break duration, then
	its `work_break_period` would be 72 hours (3 days) as its work & break
	timings repeats every 3 days.
	The robot's `work_cycle_in_days` would be 21 days as its salary amount
	repeats every 21 days.
	"""
	def get_GCD(a,b):
		# Recursive function to return gcd of a and b
		if a == 0:
			return b
		return get_GCD(b % a, a)
	
	def get_LCM(a,b):
		# Function to return LCM of two numbers
		return (a / get_GCD(a,b))* b

	work_break_period = get_LCM(work_duration_in_hours + break_duration_in_hours, 24)
	work_cycle_in_days = get_LCM(work_break_period, 7) / 24

	return work_cycle_in_days

day_1 = RobotWorkDay("07:00:00", "23:00:00", 20, 25)
day_2 = RobotShiftStartDay("2038-01-01T20:15:00", "07:00:00", "23:00:00", 20, 25)
day_3 = RobotShiftEndDay("2038-01-02T08:45:00", "07:00:00", "23:00:00", 30, 35)
day_4 = RobotWorkHalfDay("2038-01-01T03:10:00", "2038-01-01T23:45:00", "07:00:00", "23:00:00", 30, 35)
start = datetime.strptime("2038-01-01T20:15:00", "%Y-%m-%dT%H:%M:%S").strftime("%H%M")
# for i in day_1.get_break_timings("1500"): print(i)
# minutes_worked = day_1.get_minutes_worked(day_1.get_break_timings(start))
# print(minutes_worked)
# pay = day_1.calculate_pay(minutes_worked['day_minutes'], minutes_worked['night_minutes'])
# print(pay)

# for i in day_2.get_break_timings():
# 	print(1, i) 
# 	break_time = i.strftime("%H%M")
# minutes_worked = day_2.get_minutes_worked(day_2.get_break_timings())
# print(2, minutes_worked)
# pay = day_2.calculate_pay(minutes_worked['day_minutes'], minutes_worked['night_minutes'])
# print(3, pay)

# for i in day_3.get_break_timings(break_time): print(1, i)
# minutes_worked = day_3.get_minutes_worked(day_3.get_break_timings(break_time))
# print(2, minutes_worked)
# pay = day_3.calculate_pay(minutes_worked['day_minutes'], minutes_worked['night_minutes'])
# print(3, pay)


# generate_days= ['shift_start',0,1,'shift_end']

# minutes_worked = day_2.get_minutes_worked(day_2.get_break_timings())
# pay = day_2.calculate_pay(minutes_worked['day_minutes'], minutes_worked['night_minutes'])
# print("day2", pay)

# minutes_worked = day_3.get_minutes_worked(day_3.get_break_timings(break_time))
# pay = day_3.calculate_pay(minutes_worked['day_minutes'], minutes_worked['night_minutes'])
# print("day3", pay)

for i in day_4.get_break_timings(): print(i) 
minutes_worked = day_4.get_minutes_worked(day_4.get_break_timings())
print(minutes_worked)
pay = day_4.calculate_pay(minutes_worked['day_minutes'], minutes_worked['night_minutes'])
print("day4", pay)