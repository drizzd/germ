#
#  error/no_valid_keys.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from error import error

class no_valid_keys(error):
	def __init__(self):
		from germ.txt import errmsg

		error.__init__(self, error.notice, errmsg.no_valid_keys, do_log = False)
