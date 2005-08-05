#
#  choice.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from attribute import *

from error.error import *
from text import errmsg

class choice(attribute):
	def __init__(self, label, perm = {}, default = 0, options):
		attribute.__init__(self, label, perm, default)

		if len(options) == 0:
			raise error(err_fail, errmsg.attr_choice_nooptions)

		self.__options = options

	def sql_str(self):
		return str(self._val)

	def sql_type(self):
		return 'TINYINT'

	def set(self, val):
		self._val = val

	def prnt(self, str):
		return self.__options[self._val]

	def accept(self, attr_act):
		attr_act.visit_choice(self)
