#
#  invalid_parm.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from error.error import *

class invalid_key(error):
	def __init__(self, add_info = None):
		from text import errmsg
		error.__init__(self, errmsg.invalid_parm, add_info, do_log = False)
