#
#  ui_ht/attr_act_set.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from germ.attr.attr_action import *

class attr_act_set(attr_action):
	def __init__(self, val):
		self.__val = val

	def visit_sql_id(self, attr):
		attr.set(self.__val)

	def visit_text(self, attr):
		attr.set(self.__val)

	def visit_string(self, attr):
		attr.set(self.__val)

	def visit_passwd(self, attr):
		attr.set(self.__val)

	def visit_plain_pwd(self, attr):
		attr.set(self.__val)

	def visit_int(self, attr):
		attr.set(self.__val)

	def visit_choice(self, attr):
		attr.set(self.__val)

	def visit_date(self, attr):
		attr.set(self.__val)

	def visit_bool(self, attr):
		attr.set(self.__val == 'on')
