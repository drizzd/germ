#
#  error.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

err_debug, err_note, err_warn, err_error, err_fail = range(0,5)

class error(Exception):
	lang = 'en'

	def __init__(self, lvl, msg, add_info = None):
		self.__lvl = lvl
		self.__msg = msg
		self.__add_info = add_info

	def __str__(self):
		from text.errmsg import error_lvl
		return "%s: %s%s" % \
			(error_lvl[self.__lvl][error.lang],
			 self.__msg[error.lang],
			 self.__add_info is None and '' or ' (' + self.__add_info + ')')

	def __repr__(self):
		return self.__str__()
