#
#  handler.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from mod_python import apache
from mod_python import util

#from Cookie import SimpleCookie
#from mod_python import Cookie

from error import *

parm_prefix_attr = 'a_'

def handler(req):
	try:
		import cf

		req.content_type = "text/html"

		form = util.FieldStorage(req, keep_blank_values = True)

		# Hmm. First we get the action object and an entity, then the
		# parameters.
		# No action means 'just display the page', i.e. we need the 'page'
		# parameter

		p_action = form.getfirst('action', None)
		p_entity = form.getfirst('entity', None)
		p_page = form.getfirst('page', None)

#		cookies = Cookie.get_cookies(req)

		if p_action is None:
			if p_entity is not None:
				raise error(err_fail, "Request for an entity without an " +
						"action to act on it", "entity: %s" % p_entity)

			p_action = cf.ht_default_action
			p_entity = cf.ht_default_entity

		# get page

		try:
			path = cf.ht_root + '/' + cf.ht_path + '/' + cf.ht_docpath + '/'

			if p_page is not None:
				page = file(path + p_page + '.html')
			elif p_entity is not None:
				try:
					page = file(path + p_entity + '.html')
				except IOError:
					page = file(path + 'index.html')
			else:
				page = file(path + 'index.html')
		except IOError, e:
			raise error(err_fail, e, 'path: %s, page: %s, entity: %s' % \
					(path, p_page, p_entity))

		text = ''

		if p_action is None:
			while len(text = page.read(cf.buflen_max)) > 0:
				req.write(text)

			return apache.OK

		if p_entity is None:
			raise error(err_fail, "Request for an action without an " + \
					"entity to act on", "action: %s" % p_action)

		from sets import Set

		attr_map = {}
		session_vars = {}
		attr_locks = Set()
		attr_to_lock = Set()
		do_exec = False
		for name, val in [(parm.name, parm_val(parm)) for parm in form.list]:
			if name.startswith(parm_prefix_attr):
				# handle multivalued parameters
				pos = name.find('__', len(parm_prefix_attr))

				if pos < 0:
					attr = name[len(parm_prefix_attr):]

					if attr_map.has_key(attr):
						raise error(err_warn, "Multi-valued parameter " + \
								"overwritten with single-valued parameter",
								"attribute: %s" % attr)

					attr_map[attr] = val
				else:
					attr = name[len(parm_prefix_attr):pos]

					if not attr_map.has_key(attr):
						attr_map[attr] = {}
					elif not isinstance(attr_map, dict):
						raise error(err_warn, "Multi-valued parameter " + \
								"overwritten with single-valued parameter",
								"attribute: %s" % attr)

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

		mod = __import__('entity.' + p_entity, globals(), locals(),
				[p_entity])
		entity_class = getattr(mod, p_entity)

		entity = entity_class()

		entity.add_session_vars(session_vars)

		found_invalid_parm = False

		for attr, value in attr_map.iteritems():
			from error.invalid_parm import invalid_parm
			from attr_act_set import attr_act_set
			try:
				a = entity.get_attr(attr, p_action)

				a.accept(attr_act_set(value))
#				error(err_debug, 'setting attribute', 'attr: %s, val: %s' % \
#						(attr, a.get()))
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

		action_class_str = 'act_' + p_action
		try:
			mod = __import__('erm.' + action_class_str, globals(), locals(),
					[action_class_str])
			action_class = getattr(mod, action_class_str)
		except ImportError, e:
			raise error(err_fail, "Could not perform action. " + \
					"ImportError: " + str(e), "action: " + p_action)

		action = action_class(p_action, do_exec and not found_invalid_parm)

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

		print_handler = print_form

		from error.do_not_exec import do_not_exec
		from error.missing_lock import missing_lock
		from error.missing_pk_lock import missing_pk_lock
		from error.no_valid_keys import no_valid_keys
		from error.perm_denied import perm_denied
		from error.invalid_parm import invalid_parm
		prompt_pk_only = False
		try:
			entity.accept(action)

			if entity.has_rset():
				print_handler = print_list
			else:
				print_handler = print_view
		except error, e:
			if not (isinstance(e, do_not_exec) and found_invalid_parm):
				text += str(e) + "<BR />\n<BR />\n"

			if isinstance(e, missing_lock) or isinstance(e, invalid_parm):
				pass
			elif isinstance(e, do_not_exec):
				pass
			elif isinstance(e, missing_pk_lock):
				prompt_pk_only = True
			elif isinstance(e, no_valid_keys) or isinstance(e, perm_denied):
				error(err_warn, e, "action: %s, entity: %s" % \
						(p_action, p_entity))
				return apache.OK
			else:
				return boil_out(req, e)

		text += print_handler(entity, p_action, prompt_pk_only)

		req.write(text)

	except Exception, e:
		return boil_out(req, e)

	return apache.OK

def boil_out(req, e):
	# TODO: Log errors and inform administrator. Only inform user that this
	# should not happen and a bug report has been filed. Encourage user to
	# offer assistance (contact administrator, describe problem).
	#req.content_type = "text/html"
	req.write('<B>Unhandled Exception:</B> <I>%s</I>' % e)

	if isinstance(e, error):
		req.write(' (%s)' % e.err_lvl())

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

	return apache.OK

def print_view(entity, act_str, prompt_pk_only):
	last_ch = act_str[-1]
	suffix = ''

	if last_ch in ['t'] and act_str not in ['edit']:
		suffix += last_ch
	
	if last_ch != 'e':
		suffix += 'e'

	viewtext = "The following entry has been %sd.<BR />\n<BR />\n" % \
			(act_str + suffix)

	from attr_act_view import attr_act_view
	act_view = attr_act_view()

	viewtext += '<TABLE border="1">\n'

	for attr in entity.attr_iter('view'):
		viewtext += '<TR><TH align="left">%s:</TH>' % attr.label()

		viewtext += get_cell(attr, act_view)

		viewtext += "</TR>\n"

	viewtext += "</TABLE>"

	return viewtext

def get_cell(attr, act_get):
	text = '<TD>'

	attr.accept(act_get)
	attr_text = act_get.get_text()

	if attr_text == '':
		attr_text = '&nbsp;'
	
	text += attr_text

	text += '</TD>'

	return text

def print_list(entity, act_str, prompt_pk_only):
	from attr_act_view import attr_act_view
	act_view = attr_act_view()

	listtext = "<TABLE>\n"

	listtext += "\t<TR>"

	for attr in entity.attr_iter('view'):
		listtext += "<TH>%s</TH>" % attr.label()

	listtext += "</TR>\n"

	for rec in entity.rsets():
		listtext += "\t<TR>"

		for attr in rec.attr_iter('view'):
			listtext += get_cell(attr, act_view)

		listtext += "</TR>\n"

	listtext += "</TABLE>"

	return listtext

def print_form(entity, act_str, prompt_pk_only):
	import cf
	formtext = '<FORM method="GET" action="%s">\n' % ('/' + cf.ht_path + \
			'/' + cf.ht_index)

	if not prompt_pk_only:
		formtext += '<INPUT type="hidden" name="do_exec">\n'

	formtext += '<INPUT type="hidden" name="entity" value="%s">\n' % \
			entity.get_name() + \
			'<INPUT type="hidden" name="action" value="%s">\n' % act_str

	formtext += '<TABLE>\n'

	error_vec = []

	from attr_act_form_field import attr_act_form_field
	act_form_field = attr_act_form_field()
	from attr_act_form_key import attr_act_form_key
	act_form_key = attr_act_form_key()

	attr_vec = entity.get_attr_vec(act_str)
	pk_set = entity.get_pk_set()
	cnt = 0
	while len(attr_vec) > 0:
		attr_id = attr_vec.pop(0)
		attr = entity.get_attr_nocheck(attr_id)

		group = entity.get_ref_group(attr_id)

		if group is None:
			if prompt_pk_only:
				continue

			formtext += '<TR><TD colspan="2">%s:</TD><TD>' % attr.label()

			parm_name = parm_prefix_attr + attr_id

			act_form_field.set_parm_name(parm_name)
			attr.accept(act_form_field)

			formtext += act_form_field.get_text()

			formtext += get_error(attr, error_vec)

			formtext += '</TD></TR>\n'
		else:
			cnt += 1
			j = 0
			first = True
			while True:
				locked = attr.is_locked()

				formtext += '<TR><TD>%s:</TD><TD><INPUT ' \
						'type="radio" name="to_lock%u" value="%s"%s%s>' \
						'</TD><TD>' % \
							(attr.label(), cnt, attr_id,
							locked and ' disabled' or '',
							(not locked and first) and ' checked' or '')
				if locked:
					formtext += '<INPUT type="hidden" name="lock" ' \
							'value="%s">' % attr_id

				if first:
					first = False

				parm_name = parm_prefix_attr + attr_id

				if group.has_fk(attr_id):
					if prompt_pk_only and attr_id not in pk_set:
						continue

					formtext += '<SELECT name="%s"%s>' % (parm_name,
							locked and ' disabled' or '')

					cur_key = attr.sql_str()

					tmp_attr = attr.copy()

					for key in group.get_keys(attr_id):
						formtext += '\t<OPTION value="%s"%s>' % \
								(key, key == cur_key and ' selected' or '')

						tmp_attr.set_sql(key)

						error(err_debug, 'act_form_key', 'attr_id: %s, ' \
								'key: %s, attr value: %s' % \
								(attr_id, key, tmp_attr.get()))

						tmp_attr.accept(act_form_key)
						formtext += act_form_key.get_text()

						formtext += '</OPTION>\n'

					formtext += '</SELECT>'
				else:
					act_form_field.set_parm_name(parm_name)
					attr.accept(act_form_field)
					formtext += act_form_field.get_text()

				if attr.is_locked():
					# TODO: make sure this is also necessary for disabled
					# <SELECT> elements
					formtext += '<INPUT type="hidden" name="%s" value="%s">' \
							% (parm_name, attr.get())

				formtext += get_error(attr, error_vec)

				formtext += '</TD></TR>\n'

				# also display remaining attributes of the same reference
				# group
				while j < len(attr_vec) and not group.has_key(attr_vec[j]):
					j += 1

				if not (j < len(attr_vec)):
					break

				attr_id = attr_vec.pop(j)
				attr = entity.get_attr_nocheck(attr_id)

			if len(attr_vec) > 0:
				formtext += '<TR><TD colspan="2"></TD><TD><HR></TD></TR>\n'
	
	from txt import misc
	import cf

	formtext += '<TR><TD colspan="2"></TD>' \
			'<TD><INPUT type="submit" value="%s"></TD>' \
			'</TR>\n' % misc.action[act_str][cf.lang]

	formtext += '</TABLE>\n</FORM>'

	errortext = ''
	errortext += len(error_vec) > 0 and \
			"The following attributes caused errors:<BR />\n" or ''

	for i, e_vec in enumerate(error_vec):
		err_str = ''
		for e in e_vec:
			err_str += "%s<BR />\n" % e

		errortext += '<SPAN style="color: red"><SUP>%s</SUP></SPAN> %s' % \
				(i+1, err_str)

	errortext += len(error_vec) > 0 and \
			"<BR />\n" or ''

	return errortext + formtext

def get_error(attr, error_vec):
	error = attr.get_error()

	if len(error) > 0:
		error_vec.append(error)

		return '<SPAN style="color: red"><SUP>%s</SUP></SPAN>' % len(error_vec)

	return ''

def parm_val(parm):
	if isinstance(parm.file, util.FileType):
		return parm
	else:
		return util.StringField(parm.value)
