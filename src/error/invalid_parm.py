#
#  error/invalid_parm.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from error import error

class invalid_parm(error):
	def __init__(self, add_info = None):
		from txt import errmsg
		error.__init__(self, error.notice, errmsg.invalid_parm, add_info, do_log = False)
