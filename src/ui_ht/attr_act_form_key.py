#
#  ui_ht/attr_act_form_key.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from germ.attr.attr_act_get import *

class attr_act_form_key(attr_act_get):
	def __init__(self):
		attr_act_get.__init__(self)

	def visit_date(self, attr):
		from germ.lib import misc

		self._text = misc.date_str_iso(attr.get())

	def visit_bool(self, attr):
		import germ.txt.misc

		if attr.get():
			self._text = misc.yes
		else:
			self._text = misc.no
