#
#  missing_parm.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from error import *

class missing_parm(error):
	def __init__(self):
		from txt import errmsg
		error.__init__(self, err_notice, errmsg.missing_parm, do_log = False)
