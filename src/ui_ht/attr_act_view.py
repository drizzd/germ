#
#  ui_ht/attr_act_view.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from germ.attr.attr_act_get import *

class attr_act_view(attr_act_get):
	def __init__(self):
		attr_act_get.__init__(self)
	
	def visit_bool(self, attr):
		self._text = '<INPUT type="checkbox"%s disabled>' % \
				(attr.get() and ' checked' or '')

	def visit_dummy(self, attr):
		self._text = '&nbsp;'
