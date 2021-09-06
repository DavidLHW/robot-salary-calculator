from datetime import datetime, timedelta

def convert_to_datetime(iso_timestamp):
	"""
	Converts timestamps in ISO format to datetime objects.

	`iso_timestamp` are in ISO format "yyyy-MM-dd'T'hh:mm:ss"
	or simply, "%Y-%m-%dT%H:%M:%S" in datetime notation.

	"""
	# convert formatted string to datetime object
	return datetime.strptime(iso_timestamp, "%Y-%m-%dT%H:%M:%S")


class RobotWorkDay():
	"""
	Represents a particular day object.
	
	...

	Attributes
	----------
	day_start : datetime object instance
		str in "HH:MM:SS" that is converted to datetime object using `datetime.strptime()`
		represents standard day start, which is equivalent to standard night end.
	day_end : datetime object instance
		str in "HH:MM:SS" that is converted to datetime object using `datetime.strptime()`
		represents standard day start, which is equivalent to standard night end.
	day_rate : int
		Amount paid by minute in the day.
	night_rate : int
		Amount paid by minute in the night.
	time_of_last_break: str
		Time of last break taken in "HHMM". If last break is taken at
		2215 hrs, `time_of_last_break` would be "2215", defaults to "0000"
	work_duration_in_hours : int
		Duration of work in hours before it is necessary to take
		`break_duration_in_hours` hours of break, defaults to 8 hrs.
	break_duration_in_hours : int
		Duration of break in hours that is necessary after
		`work_duration_in_hours` hours of work, defaults to 1 hrs.

	Methods
	-------
	calculate_pay(day_minutes, night_minutes)
		Calculates pay of this particular Day instance.
	get_break_timings()
		Generates all the break timings for this particular Day instance.
	get_minutes_worked(break_timings)
		Generates minutes worked in the day and night.
	"""

	def __init__(
			self,
			day_start,
			day_end,
			day_rate,
			night_rate,
			time_of_last_break=None,
			work_duration_in_hours=None,
			break_duration_in_hours=None
	):
		"""
		initialise Day object

		Parameters
		----------
		day_start : datetime object instance
			str in "HH:MM:SS" that is converted to datetime object using `datetime.strptime()`
			represents standard day start, which is equivalent to standard night end.
		day_end : datetime object instance
			str in "HH:MM:SS" that is converted to datetime object using `datetime.strptime()`
			represents standard day start, which is equivalent to standard night end.
		day_rate : int
			Amount paid by minute in the day.
		night_rate : int
			Amount paid by minute in the night.
		time_of_last_break: str
			Time of last break taken in "HHMM". If last break is taken at
			2215 hrs, `time_of_last_break` would be "2215", defaults to "0000"
		work_duration_in_hours : int
			Duration of work in hours before it is necessary to take
			`break_duration_in_hours` hours of break, defaults to 8 hrs.
		break_duration_in_hours : int
			Duration of break in hours that is necessary after
			`work_duration_in_hours` hours of work, defaults to 1 hrs.
		"""

		self.day_start = datetime.strptime(day_start, "%H:%M:%S")
		self.day_end = datetime.strptime(day_end, "%H:%M:%S")
		self.day_rate = day_rate
		self.night_rate = night_rate
		
		if not work_duration_in_hours:
			self.work_duration_in_hours = 8
		else:
			self.work_duration_in_hours = work_duration_in_hours

		if not break_duration_in_hours:
			self.break_duration_in_hours = 1
		else:
			self.break_duration_in_hours = break_duration_in_hours

		if not time_of_last_break:
			self.time_of_last_break = "0000"
		else:
			self.time_of_last_break = time_of_last_break


	def calculate_pay(self, day_minutes, night_minutes):
		"""
		Calculate pay of robot for this Day instance.

		Pay is calculated based on the different rates for working
		in the day and working at night.

		Parameters
		----------
		day_minutes : int
			Number of minutes robot has worked in the day
			of this Day instance.
		night_minutes : int
			Number of minutes robot has worked in the night
			of this Day instance.

		Returns
		-------
		float
			Amount of value to pay robot
		"""
		
		day_pay = day_minutes * self.day_rate
		night_pay = night_minutes * self.night_rate
		pay = day_pay + night_pay
		return round(pay, 2)


	def get_break_timings(self):
		"""
		Finds out timings of robot breaks for this Day instance.

		Yields
		------
		datetime object instance
			Iterable generator object of strings containing datetime object
			instances of all of the timings at which robot took a break.
		"""

		# get numerical values of hour and minute for `time_of_last_break` 
		time_of_last_break = self.time_of_last_break
		last_break_hour = int(self.time_of_last_break[:2])
		last_break_minute = int(self.time_of_last_break[-2:])

		# The following is to check if given `time_of_last_break` is valid by checking if
		# it falls before the `latest_break_time` which is calculated by taking the earliest
		# time of the previous day, `datetime(1900,1,2)` and counting back the break
		# period of `break_duration_in_hours` & work period of `work_duration_in_hours`
		
		# get datetime of `latest_break_time`, taking into account work & break duration
		latest_break_time = datetime(1900,1,2)
		latest_break_time -= timedelta(hours=self.break_duration_in_hours)
		latest_break_time -= timedelta(hours=self.work_duration_in_hours)
		
		# get datetime of `time_of_last_break`
		time_of_last_break_dt = datetime.strptime(time_of_last_break, "%H%M")

		# raise error if `time_of_last_break` given falls before
		# the latest possible break time of `latest_break_time`
		if time_of_last_break_dt < latest_break_time:
			raise InvalidBreakTimeError(time_of_last_break)

		# The following will make the generator object
		# set `hours_since_break` to be hours since the start of the last break
		isBreak = False
		hours_since_break = 24 - (last_break_hour + self.break_duration_in_hours)
		break_hours_taken = 0

		# checks if its time for break at every hour of the day
		for hour in range(24):
			# `continue` until break duration is over
			if isBreak:
				break_hours_taken += 1
				if break_hours_taken == self.break_duration_in_hours:
					break_hours_taken = 0
					isBreak = False
				continue

			# when its time to take a break, append the time in "HHSS"
			if hours_since_break == self.work_duration_in_hours:
				hours_since_break = 0
				break_time = f"{hour:02d}{last_break_minute}"
				break_time_dt = datetime.strptime(break_time, "%H%M")
				isBreak = True
				yield break_time_dt
			
			hours_since_break += 1


	def get_minutes_worked(self, break_timings):
		"""
		Calculates number of minutes worked in day minutes and night minutes.

		Parameters
		----------
		break_timings : iterable object
			Generator object generated from `get_break_timings` containing
			datetime object instances of all of the timings at which robot
			took a break.

		Returns
		-------
		dict of {str : int}
			keys - "day_minutes", "night_minutes"
			values - `day_minutes`, `night_minutes`
		"""
		
		day_minutes = (self.day_end - self.day_start).seconds / 60
		night_minutes = 24*60 - day_minutes

		break_duration_td = timedelta(hours=self.break_duration_in_hours)

		for break_time in break_timings:
			# if `break_time` lies within the period of the day, remove the 
			# break duration (in minutes) from the total day_minutes, remove the
			# break duration (in minutes) from the total night_minutes otherwise.
			if self.day_start <= break_time < self.day_end - break_duration_td:
				day_minutes -= self.break_duration_in_hours*60
			else:
				night_minutes -= self.break_duration_in_hours*60

		return {"day_minutes": day_minutes, "night_minutes": night_minutes}


class RobotShiftStartDay(RobotWorkDay):
	"""
	Represents a the day object for the start of the shift.
	
	...

	Attributes
	----------
	shift_start : datetime object instance
		str in "HH:MM:SS" that is converted to datetime object using `datetime.strptime()`
		represents the start of the shift.
	day_start : datetime object instance
		str in "HH:MM:SS" that is converted to datetime object using `datetime.strptime()`
		represents standard day start, which is equivalent to standard night end.
	day_end : datetime object instance
		str in "HH:MM:SS" that is converted to datetime object using `datetime.strptime()`
		represents standard day start, which is equivalent to standard night end.
	day_rate : int
		Amount paid by minute in the day.
	night_rate : int
		Amount paid by minute in the night.
	time_of_last_break: str
		Time of last break taken in "HHMM". If last break is taken at
		2215 hrs, `time_of_last_break` would be "2215", defaults to "0000"
	work_duration_in_hours : int
		Duration of work in hours before it is necessary to take
		`break_duration_in_hours` hours of break, defaults to 8 hrs.
	break_duration_in_hours : int
		Duration of break in hours that is necessary after
		`work_duration_in_hours` hours of work, defaults to 1 hrs.

	Methods
	-------
	calculate_pay(day_minutes, night_minutes)
		Calculates pay of this particular Day instance.
	get_break_timings()
		Generates all the break timings for this particular Day instance.
	get_minutes_worked(break_timings)
		Generates minutes worked in the day and night.
	"""

	def __init__(
			self,
			shift_start,
			day_start,
			day_end,
			day_rate,
			night_rate,
			time_of_last_break=None,
			work_duration_in_hours=None,
			break_duration_in_hours=None
	):
		"""
		initialise Day object

		Parameters
		----------
		shift_start : datetime object instance
			str in "HH:MM:SS" that is converted to datetime object using `datetime.strptime()`
			represents the start of the shift.
		day_start : datetime object instance
			str in "HH:MM:SS" that is converted to datetime object using `datetime.strptime()`
			represents standard day start, which is equivalent to standard night end.
		day_end : datetime object instance
			str in "HH:MM:SS" that is converted to datetime object using `datetime.strptime()`
			represents standard day start, which is equivalent to standard night end.
		day_rate : int
			Amount paid by minute in the day.
		night_rate : int
			Amount paid by minute in the night.
		time_of_last_break: str
			Time of last break taken in "HHMM". If last break is taken at
			2215 hrs, `time_of_last_break` would be "2215", defaults to "0000"
		work_duration_in_hours : int
			Duration of work in hours before it is necessary to take
			`break_duration_in_hours` hours of break, defaults to 8 hrs.
		break_duration_in_hours : int
			Duration of break in hours that is necessary after
			`work_duration_in_hours` hours of work, defaults to 1 hrs.
		"""
		
		super().__init__(
				day_start,
				day_end,
				day_rate,
				night_rate,
				time_of_last_break,
				work_duration_in_hours,
				break_duration_in_hours
		)
		if not isinstance(shift_start, datetime):
			self.shift_start = convert_to_datetime(shift_start)
		else:
			self.shift_start = shift_start


	def get_break_timings(self):
		"""
		Finds out timings of robot breaks for this Day instance.

		Yields
		------
		datetime object instance
			Iterable generator object of strings containing datetime object
			instances of all of the timings at which robot took a break, if any.
			Otherwise, yield only `shift_start`.
		"""

		# The following is to check if given `shift_start` falls before the `latest_break_time`
		# which is calculated by time of shift start and counting back the break
		# period of `break_duration_in_hours` & work period of `work_duration_in_hours`
		
		# get numerical value of year, month, day, hour, minute & second for start of shift
		shift_start_hour = int(self.shift_start.strftime("%H"))
		shift_start_minute = int(self.shift_start.strftime("%M"))
		shift_start_year = int(self.shift_start.strftime("%Y"))
		shift_start_month = int(self.shift_start.strftime("%m"))
		shift_start_day = int(self.shift_start.strftime("%d"))

		# get datetime of `latest_break_time`, taking into account work & break duration
		latest_break_time = datetime(shift_start_year, shift_start_month, shift_start_day)
		latest_break_time += timedelta(days=1)
		latest_break_time -= timedelta(hours=self.break_duration_in_hours)
		latest_break_time -= timedelta(hours=self.work_duration_in_hours)

		# yield all break times if shift start time falls on or before latest possible
		# break time, yield shift start time otherwise.
		if self.shift_start <= latest_break_time:
			# set `hours_since_break` to be hours since the start of the last break
			# `isBreak` is set to `True` such that the last break is accounted for
			isBreak = False
			hours_since_break = 0
			break_hours_taken = 0
			
			# checks if its time for break at every hour between shift start and midnight.
			for hour in range(24 - shift_start_hour):
				# `continue` until break duration is over
				if isBreak:
					break_hours_taken += 1
					if break_hours_taken == self.break_duration_in_hours:
						break_hours_taken = 0
						isBreak = False
					continue

				# when its time to take a break, append the time in "HHSS"
				if hours_since_break == self.work_duration_in_hours:
					hours_since_break = 0
					break_time_hour = hour + shift_start_hour
					break_time = f"{break_time_hour:02d}{shift_start_minute}"
					break_time_dt = datetime.strptime(break_time, "%H%M")
					isBreak = True
					yield break_time_dt
				
				hours_since_break += 1

		else:
			yield datetime.strptime(self.shift_start.strftime("%H%M"), "%H%M")


	def get_minutes_worked(self, break_timings):
		"""
		Calculates number of minutes worked in day minutes and night minutes.

		Parameters
		----------
		break_timings : iterable object
			Generator object generated from `get_break_timings` containing
			datetime object instances of all of the timings at which robot
			took a break, if any. Otherwise, `shift_start` is given.

		Returns
		-------
		dict of {str : int}
			keys - "day_minutes", "night_minutes"
			values - `day_minutes`, `night_minutes`
		"""

		shift_start_year = int(self.shift_start.strftime("%Y"))
		shift_start_month = int(self.shift_start.strftime("%m"))
		shift_start_day = int(self.shift_start.strftime("%d"))
		shift_start_hour = int(self.shift_start.strftime("%H"))
		shift_start_minute = int(self.shift_start.strftime("%M"))
		shift_start_second = int(self.shift_start.strftime("%S"))

		day_start_hour = int(self.day_start.strftime("%H"))
		day_start_minute = int(self.day_start.strftime("%M"))
		day_start_second = int(self.day_start.strftime("%S"))

		day_end_hour = int(self.day_end.strftime("%H"))
		day_end_minute = int(self.day_end.strftime("%M"))
		day_end_second = int(self.day_end.strftime("%S"))
		
		# datetime object for start of the day on the shift start, taken with respect to the
		# same year, month and day of the shift start.		
		shift_day_start = datetime(
				shift_start_year, shift_start_month, shift_start_day,
				day_start_hour, day_start_minute, day_start_second
		)

		# datetime object for end of the day on the shift start, taken with respect to the
		# same year, month and day of the shift start.
		shift_day_end = datetime(
				shift_start_year, shift_start_month, shift_start_day,
				day_end_hour, day_end_minute, day_end_second
		)
		
		# if shift starts before start of day, `day_minutes` will be the full length of the day
		# otherwise, if shift starts in the day, `day_minutes` will be the difference of shift
		# start and day end. If shift starts after end of the day, `day_minutes` will be 0.
		if self.shift_start < shift_day_start:
			day_minutes = (self.day_end - self.day_start).seconds / 60

		elif self.shift_start < shift_day_end:
			day_minutes = (shift_day_end - self.shift_start).seconds / 60

		else:
			day_minutes = 0

		# `night_minutes` is the remainder of the difference between
		# the day's length, start of shift	and `day_minutes`.	
		night_minutes = (24 - shift_start_hour)*60 - shift_start_minute \
				- (shift_start_second / 60) - day_minutes

		break_duration_td = timedelta(hours=self.break_duration_in_hours)

		for break_time in break_timings:
			# `get_break_timings` will return `shift_start` if there isn't enough time to
			# for the robot to work for `work_duration_in_hours`.
			# This check will ignore that timing as a `break_time` since the robot has yet
			# to work for `work_duration_in_hours` to claim `break_duration_in_hours`.
			shift_start_HHMM = datetime(1900, 1, 1, shift_start_hour, shift_start_minute)
			if break_time == shift_start_HHMM:
				continue
			
			# if `break_time` lies within the period of the day, remove the 
			# break duration (in minutes) from the total day_minutes, remove the
			# break duration (in minutes) from the total night_minutes otherwise.
			if self.day_start <= break_time < self.day_end - break_duration_td:
				day_minutes -= self.break_duration_in_hours*60
			else:
				night_minutes -= self.break_duration_in_hours*60

		return {"day_minutes": day_minutes, "night_minutes": night_minutes}


class RobotShiftEndDay(RobotWorkDay):
	"""
	Represents a the day object for the end of the shift.
	
	...

	Attributes
	----------
	shift_end : datetime object instance
		str in "HH:MM:SS" that is converted to datetime object using `datetime.strptime()`
		represents the end of the shift.
	day_start : datetime object instance
		str in "HH:MM:SS" that is converted to datetime object using `datetime.strptime()`
		represents standard day start, which is equivalent to standard night end.
	day_end : datetime object instance
		str in "HH:MM:SS" that is converted to datetime object using `datetime.strptime()`
		represents standard day start, which is equivalent to standard night end.
	day_rate : int
		Amount paid by minute in the day.
	night_rate : int
		Amount paid by minute in the night.
	time_of_last_break: str
		Time of last break taken in "HHMM". If last break is taken at
		2215 hrs, `time_of_last_break` would be "2215", defaults to "0000"
	work_duration_in_hours : int
		Duration of work in hours before it is necessary to take
		`break_duration_in_hours` hours of break, defaults to 8 hrs.
	break_duration_in_hours : int
		Duration of break in hours that is necessary after
		`work_duration_in_hours` hours of work, defaults to 1 hrs.

	Methods
	-------
	calculate_pay(day_minutes, night_minutes)
		Calculates pay of this particular Day instance.
	get_break_timings()
		Generates all the break timings for this particular Day instance.
	get_minutes_worked(break_timings)
		Generates minutes worked in the day and night.
	"""
	def __init__(
			self,
			shift_end,
			day_start,
			day_end,
			day_rate,
			night_rate,
			time_of_last_break,
			work_duration_in_hours=None,
			break_duration_in_hours=None
	):
		"""
		initialise Day object

		Parameters
		----------
		shift_end : datetime object instance
			str in "HH:MM:SS" that is converted to datetime object using `datetime.strptime()`
			represents the end of the shift.
		day_start : datetime object instance
			str in "HH:MM:SS" that is converted to datetime object using `datetime.strptime()`
			represents standard day start, which is equivalent to standard night end.
		day_end : datetime object instance
			str in "HH:MM:SS" that is converted to datetime object using `datetime.strptime()`
			represents standard day start, which is equivalent to standard night end.
		day_rate : int
			Amount paid by minute in the day.
		night_rate : int
			Amount paid by minute in the night.
		time_of_last_break: str
			Time of last break taken in "HHMM". If last break is taken at
			2215 hrs, `time_of_last_break` would be "2215", defaults to "0000"
		work_duration_in_hours : int
			Duration of work in hours before it is necessary to take
			`break_duration_in_hours` hours of break, defaults to 8 hrs.
		break_duration_in_hours : int
			Duration of break in hours that is necessary after
			`work_duration_in_hours` hours of work, defaults to 1 hrs.
		"""

		super().__init__(
				day_start,
				day_end,
				day_rate,
				night_rate,
				time_of_last_break,
				work_duration_in_hours,
				break_duration_in_hours
		)
		if not isinstance(shift_end, datetime):
			self.shift_end = convert_to_datetime(shift_end)
		else:
			self.shift_end = shift_end


	def get_minutes_worked(self, break_timings):
		"""
		Calculates number of minutes worked in day minutes and night minutes.

		Parameters
		----------
		break_timings : iterable object
			Generator object generated from `get_break_timings` containing
			datetime object instances of all of the timings at which robot
			took a break, if any. Otherwise, `shift_start` is given.

		Returns
		-------
		dict of {str : int}
			keys - "day_minutes", "night_minutes"
			values - `day_minutes`, `night_minutes`
		"""

		shift_end_year = int(self.shift_end.strftime("%Y"))
		shift_end_month = int(self.shift_end.strftime("%m"))
		shift_end_day = int(self.shift_end.strftime("%d"))
		shift_end_hour = int(self.shift_end.strftime("%H"))
		shift_end_minute = int(self.shift_end.strftime("%M"))
		shift_end_second = int(self.shift_end.strftime("%S"))

		day_start_hour = int(self.day_start.strftime("%H"))
		day_start_minute = int(self.day_start.strftime("%M"))
		day_start_second = int(self.day_start.strftime("%S"))

		day_end_hour = int(self.day_end.strftime("%H"))
		day_end_minute = int(self.day_end.strftime("%M"))
		day_end_second = int(self.day_end.strftime("%S"))
		
		# datetime object for start of the day on the shift start, taken with respect to the
		# same year, month and day of the shift start.		
		shift_day_start = datetime(
				shift_end_year, shift_end_month, shift_end_day,
				day_start_hour, day_start_minute, day_start_second
		)

		# datetime object for end of the day on the shift start, taken with respect to the
		# same year, month and day of the shift start.
		shift_day_end = datetime(
				shift_end_year, shift_end_month, shift_end_day,
				day_end_hour, day_end_minute, day_end_second
		)
		
		# if shift ends before start of day, `day_minutes` will be 0. Otherwise, if shift
		# starts in the day, `day_minutes` will be the difference of day start and shfit end.
		# If shift starts after end of the day, `day_minutes` will be full length of the day.
		if self.shift_end < shift_day_start:
			day_minutes = 0

		elif self.shift_end < shift_day_end:
			day_minutes = (self.shift_end - shift_day_start).seconds / 60

		else:
			day_minutes = (self.day_end - self.day_start).seconds / 60

		# `night_minutes` is the remainder of the difference between
		# the day's length, start of shift	and `day_minutes`.	
		night_minutes = (shift_end_hour)*60 + shift_end_minute \
				+ (shift_end_second / 60) - day_minutes

		break_duration_td = timedelta(hours=self.break_duration_in_hours)

		for break_time in break_timings:
			# This check will ignore `break_time` that is after the latest possible
			# break time of `break_duration_in_hours` before shift ends.
			shift_end_HHMM = datetime(1900, 1, 1, shift_end_hour, shift_end_minute)
			if break_time > shift_end_HHMM - break_duration_td:
				continue
			
			# if `break_time` lies within the period of the day, remove the 
			# break duration (in minutes) from the total day_minutes, remove the
			# break duration (in minutes) from the total night_minutes otherwise.
			if self.day_start <= break_time < self.day_end - break_duration_td:
				day_minutes -= self.break_duration_in_hours*60
			else:
				night_minutes -= self.break_duration_in_hours*60

		return {"day_minutes": day_minutes, "night_minutes": night_minutes}


class RobotWorkHalfDay(RobotWorkDay):
	"""
	Represents a the day object for the shifts that are within a day (or simply, half-day shifts).
	
	...

	Attributes
	----------
	shift_start : datetime object instance
		str in "HH:MM:SS" that is converted to datetime object using `datetime.strptime()`
		represents the start of the shift.
	shift_end : datetime object instance
		str in "HH:MM:SS" that is converted to datetime object using `datetime.strptime()`
		represents the end of the shift.
	day_start : datetime object instance
		str in "HH:MM:SS" that is converted to datetime object using `datetime.strptime()`
		represents standard day start, which is equivalent to standard night end.
	day_end : datetime object instance
		str in "HH:MM:SS" that is converted to datetime object using `datetime.strptime()`
		represents standard day start, which is equivalent to standard night end.
	day_rate : int
		Amount paid by minute in the day.
	night_rate : int
		Amount paid by minute in the night.
	time_of_last_break: str
		Time of last break taken in "HHMM". If last break is taken at
		2215 hrs, `time_of_last_break` would be "2215", defaults to "0000"
	work_duration_in_hours : int
		Duration of work in hours before it is necessary to take
		`break_duration_in_hours` hours of break, defaults to 8 hrs.
	break_duration_in_hours : int
		Duration of break in hours that is necessary after
		`work_duration_in_hours` hours of work, defaults to 1 hrs.

	Methods
	-------
	calculate_pay(day_minutes, night_minutes)
		Calculates pay of this particular Day instance.
	get_break_timings()
		Generates all the break timings for this particular Day instance.
	get_minutes_worked(break_timings)
		Generates minutes worked in the day and night.
	"""

	def __init__(
			self,
			shift_start,
			shift_end,
			day_start,
			day_end,
			day_rate,
			night_rate,
			time_of_last_break=None,
			work_duration_in_hours=None,
			break_duration_in_hours=None
	):
		"""
		initialise Day object

		Parameters
		----------
		shift_start : datetime object instance
			str in "HH:MM:SS" that is converted to datetime object using `datetime.strptime()`
			represents the start of the shift.
		shift_end : datetime object instance
			str in "HH:MM:SS" that is converted to datetime object using `datetime.strptime()`
			represents the end of the shift.
		day_start : datetime object instance
			str in "HH:MM:SS" that is converted to datetime object using `datetime.strptime()`
			represents standard day start, which is equivalent to standard night end.
		day_end : datetime object instance
			str in "HH:MM:SS" that is converted to datetime object using `datetime.strptime()`
			represents standard day start, which is equivalent to standard night end.
		day_rate : int
			Amount paid by minute in the day.
		night_rate : int
			Amount paid by minute in the night.
		time_of_last_break: str
			Time of last break taken in "HHMM". If last break is taken at
			2215 hrs, `time_of_last_break` would be "2215", defaults to "0000"
		work_duration_in_hours : int
			Duration of work in hours before it is necessary to take
			`break_duration_in_hours` hours of break, defaults to 8 hrs.
		break_duration_in_hours : int
			Duration of break in hours that is necessary after
			`work_duration_in_hours` hours of work, defaults to 1 hrs.
		"""

		super().__init__(
				day_start,
				day_end,
				day_rate,
				night_rate,
				time_of_last_break,
				work_duration_in_hours,
				break_duration_in_hours
		)
		if not isinstance(shift_start, datetime):
			self.shift_start = convert_to_datetime(shift_start)
		else:
			self.shift_start = shift_start
		
		if not isinstance(shift_end, datetime):
			self.shift_end = convert_to_datetime(shift_end)
		else:
			self.shift_end = shift_end


	def get_break_timings(self):
		"""
		Finds out timings of robot breaks for this Day instance.

		Yields
		------
		datetime object instance
			Iterable generator object of strings containing datetime object
			instances of all of the timings at which robot took a break, if any.
			Otherwise, yield only `shift_start`.
		"""

		# The following is to check if given `shift_start` falls before the `latest_break_time`
		# which is calculated by time of shift start and counting back the break
		# period of `break_duration_in_hours` & work period of `work_duration_in_hours`
		
		# get numerical value of minute for start of shift
		shift_start_hour = int(self.shift_start.strftime("%H"))
		shift_start_minute = int(self.shift_start.strftime("%M"))

		# get datetime of `latest_break_time`, taking into account work & break duration
		work_hours = self.shift_end - self.shift_start

		# yield all break times if shift start time falls on or before latest possible
		# break time, yield shift start time otherwise.
		if work_hours > timedelta(hours=self.work_duration_in_hours):
			# set `hours_since_break` to be hours since the start of the last break
			# `isBreak` is set to `True` such that the last break is accounted for
			isBreak = False
			hours_since_break = 0
			break_hours_taken = 0

			# checks if its time for break at every hour for the duration of the shift.
			for hour in range(work_hours.seconds//3600):
				# `continue` until break duration is over
				if isBreak:
					break_hours_taken += 1
					if break_hours_taken == self.break_duration_in_hours:
						break_hours_taken = 0
						isBreak = False
					continue

				# when its time to take a break, append the time in "HHSS"
				if hours_since_break == self.work_duration_in_hours:
					hours_since_break = 0
					break_time_hour = hour + shift_start_hour
					break_time = f"{break_time_hour:02d}{shift_start_minute}"
					break_time_dt = datetime.strptime(break_time, "%H%M")
					isBreak = True
					yield break_time_dt
				
				hours_since_break += 1

		else:
			yield datetime.strptime(self.shift_start.strftime("%H%M"), "%H%M")


	def get_minutes_worked(self, break_timings):
		"""
		Calculates number of minutes worked in day minutes and night minutes.

		Parameters
		----------
		break_timings : iterable object
			Generator object generated from `get_break_timings` containing
			datetime object instances of all of the timings at which robot
			took a break, if any. Otherwise, `shift_start` is given.

		Returns
		-------
		dict of {str : int}
			keys - "day_minutes", "night_minutes"
			values - `day_minutes`, `night_minutes`
		"""

		shift_start_year = int(self.shift_start.strftime("%Y"))
		shift_start_month = int(self.shift_start.strftime("%m"))
		shift_start_day = int(self.shift_start.strftime("%d"))
		shift_start_hour = int(self.shift_start.strftime("%H"))
		shift_start_minute = int(self.shift_start.strftime("%M"))

		day_start_hour = int(self.day_start.strftime("%H"))
		day_start_minute = int(self.day_start.strftime("%M"))
		day_start_second = int(self.day_start.strftime("%S"))

		day_end_hour = int(self.day_end.strftime("%H"))
		day_end_minute = int(self.day_end.strftime("%M"))
		day_end_second = int(self.day_end.strftime("%S"))
		
		# datetime object for start of the day on the shift start, taken with respect to the
		# same year, month and day of the shift start.		
		shift_day_start = datetime(
				shift_start_year, shift_start_month, shift_start_day,
				day_start_hour, day_start_minute, day_start_second
		)

		# datetime object for end of the day on the shift start, taken with respect to the
		# same year, month and day of the shift start.
		shift_day_end = datetime(
				shift_start_year, shift_start_month, shift_start_day,
				day_end_hour, day_end_minute, day_end_second
		)
		
		# if shift starts after day ends or shift ends before day starts then `day_minutes`
		# is equal to 0.
		if (self.shift_start >= shift_day_end) or (self.shift_end <= shift_day_start):
			day_minutes = 0

		# if shift starts before day starts and shift ends after day end then `day_minutes`
		# is equal to the full length of the day.
		elif (self.shift_start < shift_day_start) and (self.shift_end > shift_day_end):
			day_minutes = (self.day_end - self.day_start).seconds / 60

		# if shift ends before day ends and shift starts after day starts, then `day_minutes`
		# is equal to the full duration of the shift.
		elif (self.shift_start > shift_day_start) and (self.shift_end < shift_day_end):
			day_minutes = (self.shift_end - self.shift_start).seconds / 60

		# if shift ends after day ends and shift starts after day starts, then `day_minutes`
		# is equal to duration between shift start and day end.
		elif (self.shift_start > shift_day_start) and (self.shift_end > shift_day_end):
			day_minutes = (shift_day_end - self.shift_start).seconds / 60
		# if shift ends after day ends and shift starts after day starts, then `day_minutes`
		# is equal to duration between day start and shift end.
		elif (self.shift_start < shift_day_start) and (self.shift_end < shift_day_end):
			day_minutes = (self.shift_end - shift_day_start).seconds / 60

		# theres literally no way this would occur
		else:
			print('unexpected error')

		# `night_minutes` is the remainder of the difference between
		# the day's length, start of shift	and `day_minutes`.	
		night_minutes = (self.shift_end - self.shift_start).seconds / 60 - day_minutes

		break_duration_td = timedelta(hours=self.break_duration_in_hours)

		for break_time in break_timings:
			# `get_break_timings` will return `shift_start` if there isn't enough time to
			# for the robot to work for `work_duration_in_hours`.
			# This check will ignore that timing as a `break_time` since the robot has yet
			# to work for `work_duration_in_hours` to claim `break_duration_in_hours`.
			shift_start_HHMM = datetime(1900, 1, 1, shift_start_hour, shift_start_minute)

			if break_time == shift_start_HHMM:
				continue
			
			# if `break_time` lies within the period of the day, remove the 
			# break duration (in minutes) from the total day_minutes, remove the
			# break duration (in minutes) from the total night_minutes otherwise.
			if self.day_start <= break_time <= self.day_end - break_duration_td:
				day_minutes -= self.break_duration_in_hours*60
			else:
				night_minutes -= self.break_duration_in_hours*60

		return {"day_minutes": day_minutes, "night_minutes": night_minutes}


class InvalidBreakTimeError(Exception):
	"""
	Exception raised for errors in the input `break_time`.

	Attributes
	----------
	break_time : str
		Input `break_time` which caused the error.
	message : str
		Explanation of the error.
	"""

	def __init__(self, break_time, message=None):
		self.break_time = break_time
		if not message:
			self.message = "Time of last break given is invalid! \n\n"+\
					"Check that your given break timing is the last break of the previous day."
		else:
			self.message = message
		super().__init__(self.message)

	def __str__(self):
		return f'"{self.break_time}" -> {self.message}'
