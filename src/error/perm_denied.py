#
#  perm_denied.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from error import error

class perm_denied(error):
	def __init__(self):
		from txt import errmsg

		error.__init__(self, error.warn, errmsg.permission_denied, do_log = False)
