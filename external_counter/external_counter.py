# *****************************************************************************
#  Copyright 2019 Dilshan R Jayakody. [jayakody2000lk@gmail.com]
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included
#  in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
# *****************************************************************************

import serial
import warnings


class ExternalCounter:
	
	DEFAULT_BAUD_RATE = 115200
	
	PACKET_ID = 94
	
	MODE_CLEAR_DISPLAY = 48
	MODE_DISPLAY = 49
	MODE_SET_TIME = 50
	MODE_SET_DATE = 51
	MODE_IDLE = 52
	MODE_SET_IDLE_MSG = 53
	MODE_SET_IDLE_TYPE = 54
	MODE_BELL = 55

	"""
	Idle mode with maximum power saving and display is completely shutdown.
	"""
	IDLE_NONE = 0

	"""
	Display system time in idle mode.
	"""
	IDLE_TIME = 1

	"""
	Display system date in the idle mode.
	"""
	IDLE_DATE = 2

	"""
	Display custom message in the idle mode.
	"""
	IDLE_MSG = 3
	
	device_port = ''
	serial_handle = None
	
	def __init__(self, port):
		self.device_port = port
		self.open_device()

	@staticmethod
	def __string_to_byte_array(instr):
		return_array = []

		for array_char in instr:
			return_array.append(ord(array_char))

		pad_count = 10 - len(return_array)
		if pad_count > 0:
			return_array.extend([0] * pad_count)

		return return_array

	def __is_device_available(self):
		if not self.serial_handle.is_open:
			raise Exception("Unable to open communication port")
			
		return True

	def __send_extended_byte_array(self, mode, data_buffer):
		if not self.is_open():
			self.open_device()
		
		data_packet = [self.PACKET_ID, mode]
		
		if len(data_buffer) > 0:
			data_packet.extend(data_buffer)
		
		if self.__is_device_available():
			self.serial_handle.write(data_packet)

	def is_open(self):
		"""
		Check device communication channel is opened or initialized.

		:return: True if device communication channel is available. False if device communication channel is closed or
		not initialized.
		"""

		return (self.serial_handle is not None) and self.serial_handle.is_open

	def clear_display(self):
		"""
		Clear all 10 digits of the display panel.

		:return: None
		"""

		self.__send_extended_byte_array(self.MODE_CLEAR_DISPLAY, [])

	def show_message(self, msg):
		"""
		Display specified string in display panel.

		:param msg: Message to display in the panel. The maximum allowed length of this string is 10.
		:return: None
		"""

		if len(msg) == 0:
			self.clear_display()
		else:
			if len(msg) > 10:
				warnings.warn("Input string is truncated to 10 characters")
				output_buffer = msg[:10]
			else:
				output_buffer = msg
				
			output_array = self.__string_to_byte_array(output_buffer)
			assert len(output_array) == 10, "Invalid message buffer size"
			self.__send_extended_byte_array(self.MODE_DISPLAY, output_array)

	def show_number(self, number):
		"""
		Display specified number in the display panel.

		:param number: Number to display in the panel.
		:return: None
		"""

		self.show_message(str(number))

	def set_time(self, time_info):
		"""
		Set time of the display unit.

		:param time_info: Time object to update the system time of the display unit.
		:return: None
		"""

		time_buffer = [time_info.hour, time_info.minute, time_info.second]
		self.__send_extended_byte_array(self.MODE_SET_TIME, time_buffer)

	def set_date(self, date_info):
		"""
		Set date of the display unit.

		:param date_info: Date object to update the system date of the display unit.
		:return: None
		"""

		date_buffer = [date_info.day, date_info.month, (date_info.year - 2000)]
		self.__send_extended_byte_array(self.MODE_SET_DATE, date_buffer)

	def set_datetime(self, datetime_info):
		"""
		Update system date and time of the display unit.

		:param datetime_info: Date/Time object to update the system date and time.
		:return: None
		"""

		self.set_time(datetime_info)
		self.set_date(datetime_info)

	def to_idle(self):
		"""
		Forcefully switch display panel to idle mode.

		:return: None
		"""

		self.__send_extended_byte_array(self.MODE_IDLE, [])

	def set_idle_message(self, msg):
		"""
		Set idle message of the display unit.

		:param msg: Idle message to display in the panel. The maximum allowed length of this string is 10.
		:return: None
		"""

		if len(msg) > 10:
			warnings.warn("Input string is truncated to 10 characters")
			output_buffer = msg[:10]
		else:
			output_buffer = msg

		output_array = self.__string_to_byte_array(output_buffer)
		assert len(output_array) == 10, "Invalid message buffer size"
		self.__send_extended_byte_array(self.MODE_SET_IDLE_MSG, output_array)

	def set_idle_number(self, number):
		"""
		Set idle message of the display unit as number.

		:param number: Idle message to display in the panel as number.
		:return: None
		"""

		self.set_idle_message(str(number))

	def set_idle_mode(self, mode):
		"""
		Set default idle mode the display panel.

		:param mode: Idle mode to set as a default.
		:return: None
		"""

		assert self.IDLE_NONE <= mode <= self.IDLE_MSG, "Invalid idle mode"
		self.__send_extended_byte_array(self.MODE_SET_IDLE_TYPE, [mode])

	def bell(self):
		"""
		Activate audio buzzer in the display panel.

		:return: None
		"""

		self.__send_extended_byte_array(self.MODE_BELL, [])

	def open_device(self, port=''):
		"""
		Open communication channel with the display panel.

		:param port: Serial communication port to link with the display panel.
		:return: None
		"""

		if port != '':
			self.device_port = port
		
		if self.is_open():
			self.serial_handle.close()
		
		if not self.device_port.strip():
			raise Exception("Communication port is not defined or object is not initialized")
		
		self.serial_handle = serial.Serial()
		self.serial_handle.port = self.device_port
		self.serial_handle.baudrate = self.DEFAULT_BAUD_RATE
		
		self.serial_handle.open()

	def close_device(self):
		"""
		Close communication channel with the display panel.

		:return: None
		"""

		if self.is_open():
			self.serial_handle.close()
