#
#  no_valid_keys.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from error import *

class no_valid_keys(error):
	def __init__(self):
		from txt import errmsg
		error.__init__(self, err_notice, errmsg.no_valid_keys, do_log = False)
