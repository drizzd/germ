#
#  ui_ht/boil_out.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from germ.error.error import error

def boil_out():
	# TODO: Log errors and inform administrator. Only inform user that this
	# should not happen and a bug report has been filed. Encourage user to
	# offer assistance (contact administrator, describe problem).

	import sys
	exc = sys.exc_info()[1]

	print '<B>Unhandled Exception:</B> <I>%s</I>' % exc

	if isinstance(exc, error):
		print ' (%s)' % error.lvl_txt(exc.lvl())
	else:
		error(error.error, str(exc))

	print '<BR />\n'

	from germ.txt import errmsg
	print errmsg.failure

	print "<PRE>"
	import traceback
	import sys
	traceback.print_exc(file = sys.stdout)
	print "</PRE>"

	import cf
	print '<HR>System Administrator: ' \
			'<A href="mailto:%s">%s</A>' % (cf.admin_email, cf.admin_email)

	from pso.service import OK
	return OK
