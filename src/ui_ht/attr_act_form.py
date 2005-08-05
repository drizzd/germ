#
#  attr_act_form.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from attr.attr_action import *

class attr_act_form(attr_action):
	def __init__(self, formtext, error_vec, attr_locks):
		self._formtext = formtext
		self._error_vec = error_vec
		self._attr_locks = attr_locks

		self._parm_name = None
		self._is_locked = None

	def set_parm_name(name):
		self._parm_name = name
		self._is_locked = name in self._attr_locks

	def _lock_str(self):
		return self._is_locked and ' disabled' or ''
