#
#  handler.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from mod_python import apache
from mod_python import util

#from Cookie import SimpleCookie
#from mod_python import Cookie

from error.error import *

def parm_val(parm):
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
						"action to act on it", "entity: %s" % entity)

			action = cf.ht_default_action
			entity = cf.ht_default_entity

		if action is None:
			if page is None:
				raise error(err_fail, "No action to execute and no page " + \
						"to display. I have nothing to do!")

			path = cf.ht_docpath + '/' + page + '.html'

			try:
				page_file = file(path)
			except IOError, e:
				raise error(err_fail, "IOError: " + str(e), "path: " + path)

			req.content_type = "text/html"

			while len(text = page_file.read(cf.buflen_max)) > 0:
				req.write(text)

			return apache.OK

		if entity is None:
			raise error(err_fail, "Request for an action without an " + \
					"entity to act on", "action: %s" % action)

		if readable("%s/%s.html" % (cf.ht_docpath, entity)
			page = entity

		__import__('entity.' + entity)

		ent = eval(entity + '.' + entity + '()')

		from sets import Set

		attr_map = {}
		session_vars = {}
		attr_locks = Set()
		attr_to_lock = Set()
		do_exec = False
		for name, val in [(parm.name, parm_val(parm)) for parm in form.list]:
			if name.startswith('a_'):
				# handle multivalued parameters
				pos = name.find('__', 2)

				if pos < 0:
					attr = name[2:]

					if attr_map.has_key(attr)
						raise error(err_warn, "Multi-valued parameter " + \
								"overwritten with single-valued parameter",
								"attribute: %s" % attr)
					attr_map[attr] = val

					break
				else:
					attr = name[2:pos]

					if not attr_map.has_key(attr)
						attr_map[attr] = {}
					attr_map[attr][name[pos+2:]] = val
			elif name.startswith('v_'):
				# TODO: implement authentication
				session_vars[name[2:]] = val
			elif name == 'lock':
				attr_locks.add(val)
			elif name.startswith('to_lock'):
				attr_to_lock.add(val)
			elif name == 'do_exec':
				do_exec = True

		invalid_parm = False
		for attr, value in attr_map:
			from error.invalid_parm import *
			try:
				ent.attr_accept(attr, attr_act_set(value))
			except invalid_parm, e:
				invalid_parm = True
				if attr in attr_locks:
					raise error(err_fail, "Locked attribute has invalid value",
							"attr: %s, error: %s" % (attr, e))
				elif attr in attr_to_lock:
					attr_to_lock.remove(attr)

		for attr in attr_locks:
			ent.attr_lock(attr)

		for attr in attr_to_lock:
			ent.attr_to_lock(attr)

		act_cls = 'act_' + action
		try:
			__import__('erm.' + act_cls)
		except ImportError, e:
			raise error(err_fail, "Could not perform action. " + \
					"ImportError: " + str(e), "action: " + action)

		act = eval(act_cls + '.' + act_cls + '(%s, %s, %s)' % \
				(action, session_vars, do_exec))

		# o check for errors/success
		# o display type (form/view/listing)
		# o get possible variables, like user id and such
		#
		# display type: form as long as there are missing parameter (PK for a
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

		# TODO: First, search for required locks (-> form). After that we still
		# need to find out if we are supposed to display the whole thing as
		# form or view/listing (distinguish view/listing by the number of
		# result sets).
		#
		# Idea: Introduce a success flag. As soon as the operation has
		# succeeded, we display the result as a view/listing (even for
		# edit/delete/submit)

		# Note: Always display locked values as disabled form elements
		# (shouldn't happen for listings)

		# Possible exceptions: missing_lock, missing_pk_lock, do_not_exec (=
		# assert), perm_denied, error (general failure; should not happen),
		# invalid_parm (handled above)

		print_handler = print_form

		from error.do_not_exec import *
		from error.missing_lock import *
		from error.missing_pk_lock import *
		from error.perm_denied import *
		prompt_pk_only = True
		try:
			try:
				ent.accept(act)

				if not invalid_parm:
					if ent.has_rset():
						print_handler = print_list
					else:
						print_handler = print_view
			except error, e:
				req.write(e + "<br>")
				raise e
		except do_not_exec, e:
			pass
		except missing_lock, e:
			pass
		except missing_pk_lock, e:
			prompt_pk_only = True
		except no_valid_keys, e:
			error(err_warn, e, "action: %s, entity: %s" % (action, entity))
			return apache.OK
		except perm_denied, e:
			error(err_warn, e, "action: %s, entity: %s" % (action, entity))
			return apache.OK

		for attr in attr_to_lock:
			if ent.attr_is_locked(attr):
				attr_locks.append(attr)

		print_handler(req, ent, attr_locks, prompt_pk_only)

	except error, e:
		# TODO: Log errors and inform administrator. Only inform user that this
		# should not happen and a bug report has been filed. Encourage user to
		# offer assistance (contact administrator, describe problem).
		req.content_type = "text/plain"
		req.write("Unhandled Exception: " + str(e))

		from text import errmsg
		req.write(errmsg.failure)
		import cf
		req.write("\nSystem Administrator: %s <%s>" % \
			(cf.admin_name, cf.admin_email))
	return apache.OK

	def print_view(req, ent, attr_locks, prompt_pk_only):
		req.write("The following entry has been &lt;whatever&gt;<BR />")

		viewtext = ""

		from attr_act_view import *
		act_view = attr_act_view(viewtext)

		viewtext += "<TABLE>"

		for attr in ent.get_attr_vec():
			viewtext += "<TR><TH>%s:</TH><TD>" % attr.label()

			ent.attr_accept(attr, act_view)

			viewtext += "</TD></TR>"

		viewtext += "</TABLE>"

	def print_list(req, ent, attr_locks, prompt_pk_only):
		listtext = ""

		from attr_act_list import *
		act_list = attr_act_view(listtext)

		listtext += "<TABLE>\n"

		listtext += "\t<TR>"

		for attr in rec.get_attr_vec():
			listtext += "<TH>%s</TH>" % attr.label()

		listtext += "</TR>\n"

		for rec in ent.rsets()
			listtext += "\t<TR>"

			for attr in rec.get_attr_vec():
				listtext += "<TD>"
				ent.attr_accept(attr, act_view)
				listtext += "</TD>"

			listtext += "</TR>\n"

		listtext += "</TABLE>"

	def print_form(req, ent, attr_locks, prompt_pk_only):
		formtext = ""
		error_vec = []

		act_form_field = attr_act_form_field(formtext, error_vec, attr_locks)
		act_form_key = attr_act_form_key(formtext, error_vec, attr_locks)

		attr_vec = ent.get_attr_vec()[:]
		from sets import Set
		pk_set = Set(ent.get_pk_vec())
		cnt = 0
		while len(attr_vec) > 0:
			attr = attr_vec.pop(0)
			group = ent.get_ref_group(attr)

			if group is None:
				if prompt_pk_only:
					continue

				act_form_field.set_parm_name(attr)
				ent.attr_accept(attr, act_form_field)
			else:
				cnt++
				j = 0
				while True:
					locked = attr in attr_locks

					if locked:
						formtext += '<INPUT type="hidden" ' + \
								'name="lock" value="%s">' % attr

					formtext += '<INPUT type="radio" name="to_lock%u" ' + \
							'value="%s"%s>' % (cnt, attr,
								locked and ' diabled' or '')

					if group.has_fk(attr):
						if prompt_pk_only and attr not in pk_vec:
							continue

						act_form = act_form_key
					else:
						act_form = act_form_field

					act_form.set_parm_name(attr)
					ent.attr_accept(attr, act_form)

					# also display remaining attributes of the same reference
					# group
					while j < len(attr_vec) and not group.has_key(attr_vec[j]):
						j++

					if not (j < len(attr_vec)):
						break

					attr = attr_vec.pop(j)

		if len(error_vec) > 0:
			req.write("The following attributes caused errors:<BR />")

		for i, e in enumerate(error_vec):
			req.write("%s: %s", (i+1, "<br>".join(e)))

		req.write(formtext)
