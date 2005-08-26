#
#  choice.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from attribute import *

from error.error import error
from txt import errmsg

class choice(attribute):
	def __init__(self, label, options, perm = [], default = 0,
			chk_func_vec = []):
		attribute.__init__(self, label, perm, default, chk_func_vec)

		if len(options) == 0:
			raise error(error.fail, errmsg.attr_choice_nooptions)

		self.__options = options

	def get_options(self):
		return self.__options

	def _sql_str(self):
		return str(self._val)

	def sql_type(self):
		return 'TINYINT'

	def _do_set(self, val):
		try:
			self._val = int(val)
		except ValueError, e:
			self._error(e)

	def __str__(self):
		from lib import misc

		return misc.txt_lang(self.__options[self._val])

	def accept(self, attr_act):
		attr_act.visit_choice(self)
