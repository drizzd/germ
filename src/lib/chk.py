#
#  chk.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

def identifier(val):
	import re

	if re.match(r'^[a-z_][a-z0-9_]*$', val.lower()) is None:
		from error import *
		from txt import errmsg
		return error(err_fail, errmsg.invalid_identifier)

	return val.lower()
