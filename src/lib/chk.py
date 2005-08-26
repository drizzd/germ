#
#  chk.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

def identifier(val):
	import re

	if re.match(r'^[a-z_][a-z0-9_]*$', val.lower()) is None:
		from error.error import error
		from txt import errmsg
		return error(error.fail, errmsg.invalid_identifier)

	return val.lower()

class greater_equal:
	err_msg = {
		'en': 'Only values greater or equal %s',
		'de': 'Nur Werte gr"o"ser gleich %s' }

	def __init__(self, comp):
		self.__comp = comp

	def __call__(self, val):
		if not int(val) >= self.__comp:
			from error.error import error
			from misc import txt_lang

			return error(error.fail, txt_lang(self.err_msg) % self.__comp)

		return val
