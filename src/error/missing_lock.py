#
#  missing_lock.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from error import error

class missing_lock(error):
	def __init__(self):
		from txt import errmsg

		error.__init__(self, error.notice, errmsg.missing_lock, do_log = False)
