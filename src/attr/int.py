#
#  int.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from attribute import *

class int(attribute):
	def __init__(self, label, perm = {}, default = None, length = 128,
			chk_func_vec = []):
		attribute.__init__(self, label, perm, default, chk_func_vec)
		self.__length = length

	def sql_str(self):
		return str(self._val)

	def sql_type(self):
		return 'INT(%u)' % self.__length

	def _do_set(self, val):
		try:
			self._val = int(val)
		except ValueError:
			self._format_error()

	def accept(self, attr_act):
		attr_act.visit_int(self)
