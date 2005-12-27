#
#  error/missing_parm.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from error import error

class missing_parm(error):
	def __init__(self):
		from germ.txt import errmsg

		error.__init__(self, error.notice, errmsg.missing_parm, do_log = False)
