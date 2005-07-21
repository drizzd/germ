#
#  attr_act_set.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from attribute.attr_action import *

class attr_act_set(attr_action):
	def __init__(self, val):
		self.__val = val

	def visit_string(attr):
		self.set(self.__val)

	def visit_int(attr):
		self.set(self.__val)

	def visit_date(attr):
		attr.set(self.__val)

	def visit_bool(attr):
		attr.set(self.__val == 'on')
