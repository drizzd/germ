#
#  bool.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from attribute import *

class bool(attribute):
	def __init__(self, label, perm = [], default = 0, chk_func_vec = []):
		attribute.__init__(self, label, perm, default, chk_func_vec)

	def _sql_str(self):
		return str(self._val)

	def sql_type(self):
		return 'BOOLEAN'

	def _do_set(self, val):
		# TODO: is this useful?
		#if not isinstance(val, bool):
		#	from error.error import error
		#	self._error(error(error.fail, 'invalid type for boolean attribute',
		#			'value: %s, type: %s' % (val, type(val))))

		self._val = val and 1 or 0

	def get(self):
		return self._val != 0

	def accept(self, attr_act):
		attr_act.visit_bool(self)
