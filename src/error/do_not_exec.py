#
#  do_not_exec.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from error.error import *

class do_not_exec(error):
	def __init__(self):
		from text import errmsg
		error.__init__(self, errmsg.do_not_exec, do_log = False)
