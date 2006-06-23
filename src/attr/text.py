#
#  attr/text.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from attribute import *

class text(attribute):
	def __init__(self, label, perm = [], default = '', chk_func_vec = []):
		attribute.__init__(self, label, perm, default, chk_func_vec)

	def _sql_str(self):
		return self._val

	def sql_type(self):
		return 'TEXT'

	def _do_set(self, val):
		self._val = val

	def accept(self, attr_act):
		attr_act.visit_text(self)
