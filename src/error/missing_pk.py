#
#  missing_pk.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from error.error import *

class missing_pk(error):
	def __init__(self):
		from text import errmsg
		error.__init__(self, errmsg.invalid_key, do_log = False)
