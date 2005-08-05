#
#  date.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from attribute import *

class date(attribute):
	import datetime
	py_date = datetime.date

	def __init__(self, label, perm = {}, default = None):
		attribute.__init__(self, label, perm, default)

	def sql_str(self):
		return self._val.strftime("%Y%m%d")

	def set(self, val):
		if not isinstance(val, dict):
			self._format_error()

		try:
			self._val = py_date(int(val['year']), int(val['month']),
				int(val['day']))
		except ValueError, e:
			self._error(e)
		except IndexError:
			self._format_error()

	def accept(self, attr_act):
		attr_act.visit_date(self)
