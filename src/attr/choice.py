#
#  attr/choice.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from attribute import *

from germ.error.error import error
from germ.txt import errmsg

class choice(attribute):
	def __init__(self, label, options, perm = [], default = 0,
			chk_func_vec = []):
		attribute.__init__(self, label, perm, default, chk_func_vec)

		if len(options) == 0:
			raise error(error.fail, errmsg.attr_choice_nooptions)

		self.__options = options
		self.__mask = range(len(options))

	def set_mask(self, mask):
		self.__mask = mask

	def get_options(self):
		for i, choice in enumerate(self.__options):
			if i in self.__mask:
				yield (i, choice)

	def _sql_str(self):
		return str(self.get())

	def sql_type(self):
		return 'TINYINT'

	def _do_set(self, val):
		try:
			self._val = int(val)
		except ValueError, e:
			self._error(e)

	def get(self):
		val = self._val

		if val not in self.__mask:
			from germ.error.error import error
			raise error(error.error, "Choice does not heed masking",
					"key: %s, mask: %s" % (val, self.__mask))

		return val

	def __str__(self):
		from germ.lib import misc

		return misc.txt_lang(self.__options[self.get()])

	def accept(self, attr_act):
		attr_act.visit_choice(self)
