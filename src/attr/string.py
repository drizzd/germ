#
#  string.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from attribute import *

class string(attribute):
	def __init__(self, label, perm = {}, default = None, length = 128):
		attribute.__init__(self, label, perm, default)
		self.__length = length

	def sql_str(self):
		return self._val

	def sql_type(self):
		return 'VARCHAR(%u)' % self.__length

	def do_set(self, val):
		self._val = val

		return True

	def accept(self, attr_act):
		attr_act.visit_string(self)
