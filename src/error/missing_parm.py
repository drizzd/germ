#
#  missing_parm.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from error.error import *

class missing_parm(error):
	def __init__(self):
		from text import errmsg
		error.__init__(self, errmsg.missing_parm, do_log = False)
