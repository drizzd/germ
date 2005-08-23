#
#  handler.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

def handler(req):
	try:
		import cf

		prevent_caching(req)
		req.content_type = "text/html"

		from log_file_apache import log_file_apache
		from error.error import error

		error.log_file = log_file_apache(req)

		from mod_python import util
		form = util.FieldStorage(req, keep_blank_values = True)

		# Hmm. First we get the action object and an entity, then the
		# parameters.
		# No action means 'just display the page', i.e. we need the 'page'
		# parameter

		p_action = form.getfirst('action', None)
		p_entity = form.getfirst('entity', None)
		p_page = form.getfirst('page', None)

		if p_action is None:
			if p_entity is not None:
				raise error(err_fail, "Request for an entity without an " +
						"action to act on it", "entity: %s" % p_entity)

			p_action = cf.ht_default_action
			p_entity = cf.ht_default_entity

		# get page

		page = None

		try:
			path = cf.ht_root + '/' + cf.ht_path + '/' + cf.ht_docpath + '/'

			if p_entity is not None:
				try:
					page = file(path + p_entity + '.html')
				except IOError:
					pass

			if page is None:
				if p_page is not None:
					page = file(path + p_page + '.html')
				else:
					page = file(path + 'index.html')
		except IOError, e:
			raise error(err_fail, e, 'path: %s, page: %s, entity: %s' % \
					(path, p_page, p_entity))

		from mod_python.Session import Session

		session = Session(req, secret = cf.ht_secret)
		session.load()

		content = ''
		if p_action is not None:
			ret = get_content(p_entity, p_action, form, session)

			if isinstance(ret, error):
				return boil_out(req, e)

			content = ret

		from ht_parser import ht_parser
		parser = ht_parser()

		parser.set_params(content, session)

		while True:
			text = page.read(cf.buflen_max)
			parser.feed(text)

			if len(text) == 0:
				break

		parser.close()

		req.write(parser.output())

	except Exception, e:
		from boil_out import boil_out
		return boil_out(req, e)

	from mod_python import apache
	return apache.OK

def prevent_caching(req):
	req.headers_out.add('Expires', 'Thu, 01 Jan 1970 00:00:00 GMT')
	req.headers_out.add('Pragma', 'no-cache')
	req.headers_out.add('Cache-Control', 'no-cache')

def parm_val(parm):
	from mod_python import util

	if isinstance(parm.file, util.FileType):
		return parm
	else:
		return util.StringField(parm.value)

def get_content(p_entity, p_action, form, session):
	if p_entity is None:
		raise error(err_fail, "Request for an action without an " + \
				"entity to act on", "action: %s" % p_action)

	from sets import Set
	import cf

	attr_map = {}
	attr_locks = Set()
	attr_to_lock = Set()
	do_exec = False
	for name, val in [(parm.name, parm_val(parm)) for parm in form.list]:
		if name.startswith(cf.ht_parm_prefix_attr):
			# handle multivalued parameters
			pos = name.find('__', len(cf.ht_parm_prefix_attr))

			if pos < 0:
				attr = name[len(cf.ht_parm_prefix_attr):]

				if attr_map.has_key(attr):
					raise error(err_warn, "Multi-valued parameter " + \
							"overwritten with single-valued parameter",
							"attribute: %s" % attr)

				attr_map[attr] = val
			else:
				attr = name[len(cf.ht_parm_prefix_attr):pos]

				if not attr_map.has_key(attr):
					attr_map[attr] = {}
				elif not isinstance(attr_map, dict):
					raise error(err_warn, "Multi-valued parameter " + \
							"overwritten with single-valued parameter",
							"attribute: %s" % attr)

				attr_map[attr][name[pos+2:]] = val
		elif name == 'lock':
			attr_locks.add(val)
		elif name.startswith('to_lock'):
			attr_to_lock.add(val)
		elif name == 'do_exec':
			do_exec = True

	from erm.helper import get_entity
	entity = get_entity(p_entity, session, globals())

	found_invalid_parm = False

	for attr, value in attr_map.iteritems():
		from error.invalid_parm import invalid_parm
		try:
			a = entity.get_attr(attr, p_action)

			from attr_act_set import attr_act_set

			a.accept(attr_act_set(value))
		except invalid_parm, e:
			found_invalid_parm = True

			if attr in attr_locks:
				raise error(err_fail, "Locked attribute has invalid value",
						"attr: %s, error: %s" % (attr, e))
			elif attr in attr_to_lock:
				attr_to_lock.remove(attr)

	for attr in attr_locks:
		entity.get_attr(attr, p_action).lock()

	for attr in attr_to_lock:
		entity.get_attr(attr, p_action).to_lock()

	from erm.helper import get_action
	action = get_action(p_action, do_exec and not found_invalid_parm)

	# o check for errors/success
	# o display type (form/view/listing)
	# o get possible variables, like user id and such
	#
	# display type: form as long as there are missing parameter (PK for a
	# view, ...), view as soon as everything is okay, or a listing for
	# result sets

	# First, search for required locks (-> form). After that we still need
	# to find out if we are supposed to display the whole thing as form or
	# view/listing (distinguish view/listing by the number of result sets).
	#
	# As soon as the operation has succeeded, we display the result as a
	# view/listing (even for edit/delete/submit)

	# Note: Always display locked values as disabled form elements
	# (shouldn't happen for listings)

	content = ''

	from error.error import error
	prompt_pk_only = False
	try:
		entity.accept(action)

		if entity.has_rset():
			from print_handlers import print_list
			print_handler = print_list
		else:
			from print_handlers import print_view
			print_handler = print_view
	except error, e:
		from print_handlers import print_form
		print_handler = print_form

		from error.do_not_exec import do_not_exec
		from error.missing_lock import missing_lock
		from error.missing_pk_lock import missing_pk_lock
		from error.no_valid_keys import no_valid_keys
		from error.perm_denied import perm_denied
		from error.invalid_parm import invalid_parm

		if not (isinstance(e, do_not_exec) and found_invalid_parm):
			content += str(e) + "<BR />\n<BR />\n"

		if isinstance(e, missing_lock) or isinstance(e, invalid_parm):
			pass
		elif isinstance(e, do_not_exec):
			pass
		elif isinstance(e, missing_pk_lock):
			prompt_pk_only = True
		elif isinstance(e, no_valid_keys) or isinstance(e, perm_denied):
			from error import *
			error(err_warn, e, "action: %s, entity: %s" % \
					(p_action, p_entity))

			return content
		else:
			return e

	content += print_handler(entity, p_action, prompt_pk_only)

	session.save()

	from error import *
	error(err_debug, 'saving session')


	return content
