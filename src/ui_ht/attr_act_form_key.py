#
#  attr_act_form_key.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from attr.attr_act_get import *

class attr_act_form_key(attr_act_get):
	def __init__(self):
		attr_act_get.__init__(self)

	def visit_string(self, attr):
		self._text = attr.sql_str()

	def visit_int(self, attr):
		self._text = attr.sql_str()

	def visit_date(self, attr):
		self._text = attr.sql_str()

	def visit_bool(self, attr):
		import txt.misc

		if attr.get():
			self._text = misc.yes
		else:
			self._text = misc.no
