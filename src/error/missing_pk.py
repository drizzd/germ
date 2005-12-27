#
#  error/missing_pk.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from error import error

class missing_pk(error):
	def __init__(self):
		from germ.txt import errmsg

		error.__init__(self, error.notice, errmsg.invalid_key, do_log = False)
