#
#  do_not_exec.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from error import *

class do_not_exec(error):
	def __init__(self):
		from txt import errmsg
		error.__init__(self, err_notice, errmsg.do_not_exec, do_log = False)
