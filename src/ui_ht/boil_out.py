#
#  boil_out.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from error import *

def boil_out(req, e):
	# TODO: Log errors and inform administrator. Only inform user that this
	# should not happen and a bug report has been filed. Encourage user to
	# offer assistance (contact administrator, describe problem).
	#req.content_type = "text/html"
	req.write('<B>Unhandled Exception:</B> <I>%s</I>' % e)

	if isinstance(e, error):
		req.write(' (%s)' % error.lvl_txt(e.lvl()))
	else:
		error(err_error, str(e))

	req.write('<BR />\n')

	from txt import errmsg
	req.write(errmsg.failure)

	req.write('<BR />\n')

	req.write("<PRE>")
	import traceback
	traceback.print_exc(file=req)
	req.write("</PRE>")

	import cf
	req.write('<BR />\n<HR>System Administrator: ' \
			'<A href="mailto:%s">%s</A>' % (cf.admin_email, cf.admin_name))

	from mod_python import apache
	return apache.OK

