#
#  ui_ht/handler.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from germ.error.error import error

# TODO: Move this somewhere else.
def convert_html(text):
	import re

	text = re.sub(r'``', '"', text)
	text = re.sub(r'\'\'', '"', text)
	text = re.sub(r'"s', '&szlig;', text)
	text = re.sub(r'"([A-Za-z])', r'&\1uml;', text)

	return text

def handler(req):
	from log_file import log_file

	error.log_file = log_file()

	from germ.lib import misc
	misc.txt_lang_convert.append(convert_html)

	try:
		import cf

		prevent_caching(req)

		req.pso().send_http_header()

		import cgi
		form = cgi.FieldStorage(keep_blank_values = True)

		# Get index.

		wholename = cf.ht_docpath + '/index.html'

		index = None

		try:
			index = file(wholename)
		except IOError, e:
			raise error(error.fail, e, 'Could not open index file "%s"' % \
					wholename)

		#try:
		#	req.pso().session['reloads'] += 1
		#except:
		#	req.pso().session['reloads'] = 1

		#session = req.pso().session
		from pso.session import CookieFileImpl
		session = req.pso().getSession(CookieFileImpl,
				PSOSessionFileLoader_Path=cf.ht_tmp_path)

		ret = get_content(form, session)

		if isinstance(ret, bool):
			return ret

		content = ret

		from ht_parser import ht_parser
		parser = ht_parser()

		parser.set_params(content, session)

		while True:
			text = index.read()

			if not len(text) > 0:
				break

			parser.feed(text)

		parser.close()

		print parser.output()
	except:
		from boil_out import boil_out
		return boil_out()

	from pso.service import OK
	return OK

# Obsolete?
def prevent_caching(req):
	req.setHeaderOut('Expires', 'Thu, 01 Jan 1970 00:00:00 GMT')
	req.setHeaderOut('Pragma', 'no-cache')
	req.setHeaderOut('Cache-Control', 'no-cache')

# Obsolete?
def parm_val(parm):
	if parm.file:
		return parm.file
	else:
		return parm.value

def get_page(page):
	import cf
	path = cf.ht_docpath + '/'

	wholename = path + page + '.html'

	try:
		return file(wholename)
	except IOError:
		return None

def get_content(form, session):
	import cf

	# First we get the action object and an entity, then the parameters.
	# No action means 'just display the page', i.e. we need the 'page'
	# parameter.

	p_action = form.getfirst('action', None)
	p_entity = form.getfirst('entity', None)
	p_page = form.getfirst('page', None)

	fullpage = form.has_key('fullpage')

	if p_action is None:
		if p_entity is not None:
			raise error(error.fail, "Request for an entity without an " +
					"action to act on it", "entity: %s" % p_entity)

		if p_page is None:
			p_page = cf.ht_default_page
			p_action = cf.ht_default_action
			p_entity = cf.ht_default_entity
	elif p_entity is None:
		raise error(error.fail, "Request for an action without an " \
				"entity to act on", "action: %s" % p_action)

	# Get page.

	page = None

	if p_page is not None:
		page = get_page(p_page)

	if page is None and p_entity is not None:
		page = get_page(p_entity)

	if p_action is None:
		pagetext = ''

		if page is not None:
			while True:
				text = page.read()

				if not len(text) > 0:
					break

				pagetext += text

		return pagetext

	# Parse GET parameters.

	from sets import Set

	attr_map = {}
	attr_locks = Set()
	attr_to_lock = Set()
	do_exec = False
	for name, val in [(parm.name, parm_val(parm)) for parm in form.list]:
		if name.startswith(cf.ht_parm_prefix_attr):
			# Handle multivalued parameters.
			pos = name.find('__', len(cf.ht_parm_prefix_attr))

			if pos < 0:
				attr = name[len(cf.ht_parm_prefix_attr):]

				if attr_map.has_key(attr):
					if isinstance(attr_map[attr], dict):
						raise error(error.error, "Multi-valued parameter " \
								"overwritten with single-valued parameter",
								"attribute: %s" % attr)
					else:
						# If a single-valued parameter is specified multiple
						# times, the last occurence counts.
						pass

				attr_map[attr] = val
			else:
				attr = name[len(cf.ht_parm_prefix_attr):pos]

				if not attr_map.has_key(attr):
					attr_map[attr] = {}
				elif not isinstance(attr_map[attr], dict):
					raise error(error.error, "Single-valued parameter " \
							"overwritten with multi-valued parameter",
							"attribute: %s" % attr)

				attr_map[attr][name[pos+2:]] = val
		elif name == 'lock':
			attr_locks.add(val)
		elif name.startswith('to_lock'):
			attr_to_lock.add(val)
		elif name == 'do_exec':
			do_exec = True

	from germ.erm.helper import get_entity
	entity = get_entity(p_entity, session, globals())

	found_invalid_parm = False

	for attr, value in attr_map.iteritems():
		from germ.error.invalid_parm import invalid_parm
		try:
			a = entity.get_attr(attr, p_action)

			from attr_act_set import attr_act_set

			a.accept(attr_act_set(value))
		except invalid_parm, e:
			found_invalid_parm = True

			if attr in attr_locks:
				raise error(error.fail, "Locked attribute has invalid value",
						"attr: %s, error: %s" % (attr, e))
			elif attr in attr_to_lock:
				attr_to_lock.remove(attr)

	for attr in attr_locks:
		entity.get_attr(attr, p_action).lock()

	for attr in attr_to_lock:
		entity.get_attr(attr, p_action).to_lock()

	from germ.erm.helper import get_action
	action = get_action(p_action, do_exec and not found_invalid_parm)

	# o Check for errors/success
	# o Display type (form/view/listing)
	# o Get possible variables, like user id and such
	#
	# Display type: Form as long as there are missing parameters (PK for a
	# view, ...), view as soon as everything is okay, or a listing for
	# result sets

	# First, search for required locks (-> form). After that we still need
	# to find out if we are supposed to display the whole thing as form or
	# view/listing (distinguish view/listing by the number of result sets).
	#
	# As soon as the operation has succeeded, we display the result as a
	# view/listing (even for edit/delete/submit).

	# Note: Always display locked values as disabled form elements
	# (shouldn't happen for listings).

	error_str = ''
	display_errors = True

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

		from germ.error.do_not_exec import do_not_exec
		from germ.error.missing_lock import missing_lock
		from germ.error.missing_pk_lock import missing_pk_lock
		from germ.error.no_valid_keys import no_valid_keys
		from germ.error.perm_denied import perm_denied
		from germ.error.invalid_parm import invalid_parm

		if (isinstance(e, do_not_exec) or isinstance(e, invalid_parm)) \
				and (not do_exec or found_invalid_parm):
			display_errors = False

		error_str = str(e) + "<BR />\n<BR />\n"

		if isinstance(e, missing_lock):
			if not do_exec:
				error_str = str(do_not_exec()) + "<BR />\n<BR />\n"
		elif isinstance(e, invalid_parm):
			pass
		elif isinstance(e, do_not_exec):
			pass
		elif isinstance(e, missing_pk_lock):
			prompt_pk_only = True
		elif isinstance(e, no_valid_keys) or isinstance(e, perm_denied):
			error(error.warn, e, "action: %s, entity: %s" % \
					(p_action, p_entity))

			return error_str
		else:
			import sys
			exctype, exc, tb = sys.exc_info()
			raise exctype, exc, tb

	print_parm = {
			'handler': print_handler,
			'entity': entity,
			'action': p_action,
			'page': p_page,
			'prompt_pk_only': prompt_pk_only,
			'display_errors': display_errors,
			'error_str': error_str }

	if page is None:
		from print_handlers import do_print

		output = do_print(**print_parm)
	else:
		from ht_cont_parser import ht_cont_parser
		parser = ht_cont_parser()

		parser.set_params(session, print_parm)

		while True:
			text = page.read()

			if not len(text) > 0:
				break

			parser.feed(text)

		parser.close()

		output = parser.output()

	session.save()

	return output
