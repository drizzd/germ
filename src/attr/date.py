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

	def do_set(self, val):
		if not (isinstance(val, dict) and
			val.has_key('year') and
			val.has_key('month') and
			val.has_key('day')):
			return False

		self._val = py_date(val['year'], val['month'], val['day'])

		return True

	def accept(self, attr_act):
		attr_act.visit_date(self)
