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

		# hmm. first we need to know the action, then possibly an entity, then
		# the parameters
		# no action means 'just display the page', i.e. we need the 'page'
		# parameter

		entity = form.getfirst('entity')
		if entity is None:
			page = form.getfirst('page', 'index')
		else:
			# make this a default template if no custom html file exists
			page = entity

		action = form.getfirst('action')

#		cookies = Cookie.get_cookies(req)

		req.content_type = "text/html"

		if entity is not None:
			if action is None:
				import text.errmsg
				raise error(err_fail, errmsg.missing_parm, 'action')
			else:
				entity_actions = ['edit', 'submit', 'delete', 'view', 'list', 'listedit']
				if action not in entity_actions

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

			...
			req.write("entity = " + entity + "\n")
		if action is not None:
			req.write("action = " + action + "\n")
		test_fn(req)

	except error, e:
		# TODO: Log errors and inform administrator. Only inform user that this
		# should not happen and a bug report has been filed. Encourage user to
		# offer assistance (contact administrator, describe problem).
		req.write('germ: ' + str(e))
	return apache.OK
