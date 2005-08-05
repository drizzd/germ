#
#  bool.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from attribute import *

class bool(attribute):
	def __init__(self, label, perm = {}, default = 0):
		attribute.__init__(self, label, perm, default)

	def sql_str(self):
		return str(self._val)

	def sql_type(self):
		return 'BOOLEAN'

	def set(self, val):
		self._val = val and 1 or 0

	def get(self, str):
		return self._val != 0

	def accept(self, attr_act):
		attr_act.visit_bool(self)
