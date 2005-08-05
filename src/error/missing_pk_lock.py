#
#  missing_pk_lock.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from error.error import *

class missing_pk_lock(error):
	def __init__(self):
		from text import errmsg
		error.__init__(self, errmsg.missing_pk_lock, do_log = False)
