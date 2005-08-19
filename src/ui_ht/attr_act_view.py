#
#  attr_act_view.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from attr.attr_act_get import *

class attr_act_view(attr_act_get):
	def __init__(self):
		attr_act_get.__init__(self)
	
	def visit_passwd(self, attr):
		self._text = 8*'*'

	def visit_string(self, attr):
		self._text = attr.sql_str()

	def visit_choice(self, attr):
		self._text = str(attr)

	def visit_int(self, attr):
		self._text = attr.sql_str()

	def visit_date(self, attr):
		date = attr.get()
		self._text = date.strftime("%Y-%m-%d")

	def visit_bool(self, attr):
		self._text = '<INPUT type="checkbox"%s disabled>' % \
				attr.get() and ' checked' or ''
