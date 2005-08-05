#
#  perm_denied.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from error.error import *

class perm_denied(error):
	def __init__(self):
		from text import errmsg
		error.__init__(self, errmsg.permission_denied, do_log = False)
