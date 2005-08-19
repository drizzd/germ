#
#  chk.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

def identifier(val):
	import re

	if not re.compile(r'(^[a-z_]|[^a-z0-9_])').match(val):
		from error import *
		from txt import errmsg
		return error(err_fail, errmsg.invalid_identifier, "'%s'" % val)

	return False
