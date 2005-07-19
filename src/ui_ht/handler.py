#
#  handler.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from mod_python import apache
from mod_python import util

#from Cookie import SimpleCookie
#from mod_python import Cookie

from ui_ht_test import test_fn
from lib.error import *

def handler(req):
	try:
		form = util.FieldStorage(req, keep_blank_values = True)

		entity = form.get('entity', None)
		if entity is None:
			page = form.get('page', 'index')
		else:
			page = entity
#			page = entity.get_name()

		action = form.get('action', None)
		if action is None and entity is not None:
				import text.errmsg
				raise error(err_fail, errmsg.missing_parm, 'action')

#		cookies = Cookie.get_cookies(req)

		req.content_type = "text/plain"
		if entity is not None:
			req.write("entity = " + entity + "\n")
		if action is not None:
			req.write("action = " + action + "\n")
		test_fn(req)

	except error, e:
		req.write('germ: ' + str(e))
	return apache.OK
