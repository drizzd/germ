#
#  error/invalid_key.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from error import error

class invalid_key(error):
	def __init__(self):
		from germ.txt import errmsg
		error.__init__(self, error.notice, errmsg.invalid_key, do_log = False)
