

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


class InvalidShiftError(Exception):
	"""
	Exception raised when `shift_start` occurs after `shift_end`.

	Attributes
	----------
	shift_start : datetime object instance
		The input start of shift that caused the error.
	shift_end : datetime object instance
		The input end of shift that caused the error.
	message : str
		Explanation of the error.
	"""

	def __init__(self, shift_start, shift_end, message=None):
		self.shift_start = shift_start
		self.shift_end = shift_end

		if not message:
			self.message = "Shift duration given is invalid! \n\n"+\
					"Check that the specified shift starts before it ends."
		else:
			self.message = message
		
		super().__init__(self.message)

	def __str__(self):
		return f'"{self.shift_start} to {self.shift_end}" -> {self.message}'