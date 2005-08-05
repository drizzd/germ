#
#  attr_act_form_field.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from attr_act_form import *

class attr_act_form_field(attr_act_form):
	def __init__(self, formtext, error_vec, attr_locks):
		attr_act_form.__init__(self, formtext, error_vec, attr_locks)

	def generic_text(self):
		self._formtext += '<INPUT type="text" name="%s" value="%s"%s><br>\n' % \
				(self._parm_name, attr.get(), self._lock_str())
		self._parm_name = None

	def visit_string(attr):
		self.generic_text()

	def visit_int(attr):
		self.generic_text()

	def visit_date(attr):
		date = attr.get()
		self._formtext += '-'.join(['<INPUT type="text" name="a_%s__%s" ' + \
				'length="%s" value="%s"%s>' % (self._parm_name, val_str, length,
					val, self._lock_str()) for (val_str, length, val) in
					[('year', 4, date.year), ('month', 2, date.month),
					('day', 2, date.day)]] + "<br />\n"

	def visit_bool(attr):
		self._formtext += '<INPUT type="checkbox" name="a_%s"%s%s><br />\n' % \
				(self._parm_name, attr.get() and ' checked' or '',
					self._lock_str())
