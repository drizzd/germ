#
#  attr/date.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from attribute import *

class date(attribute):
	from germ.lib import misc

	def __init__(self, label, perm = [], default = misc.today,
			chk_func_vec = []):
		attribute.__init__(self, label, perm, default, chk_func_vec)

	def _sql_str(self):
		from germ.lib import misc

		return misc.date_str_sql(self._val)

	def sql_type(self):
		return 'DATE'

	def _do_set(self, val):
		import datetime
		py_date = datetime.date

		if val is None:
			return

		if isinstance(val, py_date):
			self._val = val
		elif isinstance(val, dict):
			try:
				self._val = py_date(int(val['year']), int(val['month']),
						int(val['day']))
			except ValueError, e:
				self._error(e)
			except IndexError:
				self._format_error()
		elif isinstance(val, str):
			import re

			m = re.match('^(\d+)-(\d+)-(\d+)$', val)

			if m is None:
				self._format_error()
				return

			try:
				self._val = py_date(*m.groups())
			except e:
				self._error(e)
		else:
			self._format_error()

	def accept(self, attr_act):
		attr_act.visit_date(self)
