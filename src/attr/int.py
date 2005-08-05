#
#  int.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from attribute import *

class int(attribute):
	def __init__(self, label, perm = {}, default = None, length = 128):
		attribute.__init__(self, label, perm, default)
		self.__val = None
		self.__length = length

	def sql_str(self):
		return str(self.__val)

	def sql_type(self):
		return 'INT(%u)' % self.__length

	def set(self, val):
		self.__val = val

	def accept(self, attr_act):
		attr_act.visit_int(self)
