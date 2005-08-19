#
#  missing_lock.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from error import *

class missing_lock(error):
	def __init__(self):
		print dir()
		from txt import errmsg
		error.__init__(self, err_notice, errmsg.missing_lock, do_log = False)
