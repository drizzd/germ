#
#  error/do_not_exec.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from error import error

class do_not_exec(error):
	def __init__(self):
		from txt import errmsg
		error.__init__(self, error.notice, errmsg.do_not_exec, do_log = False)
