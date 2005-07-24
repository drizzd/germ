#
#  handler.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from mod_python import apache
from mod_python import util

#from Cookie import SimpleCookie
#from mod_python import Cookie

from lib.error import *

def get_parm_val(parm):
	if isinstance(parm.file, FileType):
		return parm
	else:
		return StringField(parm.value)

def handler(req):
	try:
		import cf

		form = util.FieldStorage(req, keep_blank_values = True)

		# Hmm. First we get the action object and an entity, then the
		# parameters.
		# No action means 'just display the page', i.e. we need the 'page'
		# parameter

		action = form.getfirst('action', None)
		entity = form.getfirst('entity', None)
		page = form.getfirst('page', cf.ht_default_page)

#		cookies = Cookie.get_cookies(req)

		if action is None:
			if entity is not None:
				raise error(err_fail, "Request for an entity without an " +
					"action to act on it", "entity = %s" % entity)

			action = cf.ht_default_action
			entity = cf.ht_default_entity

		if action is None:
			if page is None:
				raise error(err_fail, "No action and no page to display. I " +
					"don't know what to do!")

			path = cf.ht_docpath + '/' + page + '.html'

			try:
				page_file = file(path)
			except IOError, e:
				raise error(err_fail, "IOError: " + str(e), "path = " + path)

			req.content_type = "text/html"

			while len(text = page_file.read(cf.buflen_max)) > 0:
				req.write(text)

			return apache.OK

		if entity is None:
			raise error(err_fail, "Request for an action without an " +
				"entity to act on", "action = %s" % action)

		if readable("%s/%s.html" % (cf.ht_docpath, entity)
			page = entity

		__import__('entity.' + entity)

		ent = eval(entity + '.' + entity + '()')

		attr_map = {}
		attr_locks = []
		for parm in form.list:
			name = parm.name

			if name.startswith('a_'):
				val = get_parm_val(parm)

				# handle multivalued parameters
				pos = name.find('__', 2)

				if pos < 0:
					attr = name[2:]

					if attr_map.has_key(attr)
						raise error(err_warn, "Overwriting multi-valued " +
							"with single-valued parameter",
							"attribute = %s" % attr)
					attr_map[attr] = val

					break
				else:
					attr = name[2:pos]

					if not attr_map.has_key(attr)
						attr_map[attr] = {}
					attr_map[attr][name[pos+2:]] = val
			elif name.startswith('l_'):
				attr_locks.append(name[2:])

		for name, value in attr_map:
			# TODO: Don't raise an error if attribute doesn't exist. We
			# don't want the user to spy on secret attributes
			attr = ent.get_attr(name)
			attr.accept(attr_act_set(value))

		for a in parm_locks:
			attr = ent.get_attr(a)
			attr.lock()

		act_cls = 'act_' + action
		__import__('erm.' + act_cls)

		act = eval(act_cls + '.' + act_cls + '(%s)' % action)

		ent.accept(act)

		# *** response ***
		#
		# o check for errors/success
		# o display type (form/view/listing)
		# o get possible variables, like user id and such
		#
		# display type: form as long as there are missing parameters (pk for a
		# view, ...), view as soon as everything is okay, or a listing for
		# result sets
		#
		# maybe we could implement all this by giving the action a display
		# object which will then be called for generating a form/view/listing
		# as appropriate
		# => bad idea. this would require knowledge of the user interface in
		# the germ part
		#
		# we will simply have to handle the result ourselves
		#
		# In the hypter text user interface we need a HTML listing to
		# substitute the content tag and a possibly a title



		req.write("action = " + str(action) + "\n")

	except error, e:
		# TODO: Log errors and inform administrator. Only inform user that this
		# should not happen and a bug report has been filed. Encourage user to
		# offer assistance (contact administrator, describe problem).
		req.write('germ: ' + str(e))
	return apache.OK
