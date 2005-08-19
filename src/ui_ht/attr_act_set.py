#
#  attr_act_set.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from attr.attr_action import *

class attr_act_set(attr_action):
	def __init__(self, val):
		self.__val = val

	def visit_string(self, attr):
		attr.set(self.__val)

	def visit_passwd(self, attr):
		if self.__val != '':
			attr.set(self.__val)

	def visit_int(self, attr):
		attr.set(self.__val)

	def visit_choice(self, attr):
		attr.set(self.__val)

	def visit_date(self, attr):
		attr.set(self.__val)

	def visit_bool(self, attr):
		attr.set(self.__val == 'on')
