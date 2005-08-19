#
#  string.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from attribute import *

class string(attribute):
	def __init__(self, label, perm = {}, default = '', length = 128,
			chk_func_vec = []):
		attribute.__init__(self, label, perm, default, chk_func_vec)

		self.__length = length

	def sql_str(self):
		return self._val

	def sql_type(self):
		return 'VARCHAR(%u)' % self.__length

	def get_length(self):
		return self.__length

	def _do_set(self, val):
		self._val = val

	def accept(self, attr_act):
		attr_act.visit_string(self)
