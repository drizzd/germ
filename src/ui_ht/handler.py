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

def get_parm_val(parm):
	if isinstance(parm.file, FileType):
		return parm
	else:
		return StringField(parm.value)

def handler(req):
	try:
		form = util.FieldStorage(req, keep_blank_values = True)

		# Hmm. First we get the action object, then possibly an entity, then
		# the parameters. The action object will complain if the entity or
		# parameters are missing
		# No action means 'just display the page', i.e. we need the 'page'
		# parameter

		action = form.getfirst('action')
		entity = form.getfirst('entity')

		if action is not None and entity is not None:
			import cf
			if readable("%s/%s.html" % (cf.ht_docpath, entity)
				page = entity

#		cookies = Cookie.get_cookies(req)

		if action is None:
			page = form.getfirst('page', 'index')
		else:
			if entity is not None:
			__import__('entity.' + entity)

			ent = eval(entity + '.' + entity + '()')

			for a in ent.get_attr_vec():
				val = None
				lock = False

				for parm in form.list:
					name = parm.name
					if name.startswith('a_' + a):
						# handle locks and multivalued parameters
						if name == a:
							val = get_parm_val(parm)
							break
						elif len(name) > len(a) + 1 and parm[len(a)] == '_':
							if val is None:
								val = {}
							val[name[len(a)+1:]] = get_parm_val(parm)
					elif name == 'l_' + a:
						lock = True

				if val is not None:
					attr = ent.get_attr(a)
					attr.accept(attr_act_set(val))
					if lock:
						attr.lock()

			act_cls = 'act_' + action
			__import__('erm.' + act_cls)

			act = eval(act_cls + '.' + act_cls + '(%s)' % action)

			ent.accept(act)

			#...

		req.content_type = "text/html"

		req.write("action = " + str(action) + "\n")

	except error, e:
		# TODO: Log errors and inform administrator. Only inform user that this
		# should not happen and a bug report has been filed. Encourage user to
		# offer assistance (contact administrator, describe problem).
		req.write('germ: ' + str(e))
	return apache.OK
