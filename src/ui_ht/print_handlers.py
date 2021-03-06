#
#  ui_ht/print_handlers.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

def do_print(handler, entity, action, page, prompt_pk_only, display_errors,
		error_str):
	content, errortext = handler(entity, action, page, prompt_pk_only,
			display_errors)
	error_str += errortext

	if display_errors:
		return error_str + content
	else:
		return content

def get_error(attr, error_vec):
	error = attr.get_error()

	if len(error) > 0:
		error_vec.append(error)

		return '<SPAN style="color: red"><SUP>%s</SUP></SPAN>' % len(error_vec)

	return ''

def get_cell(attr, act_get):
	text = '<TD>'

	attr.accept(act_get)
	attr_text = act_get.get_text()

	if attr_text == '':
		attr_text = '&nbsp;'
	
	text += attr_text

	text += '</TD>'

	return text

def print_view(entity, act_str, page, prompt_pk_only, display_errors):
	viewtext = ''

	from germ.lib.misc import txt_lang

	report = txt_lang(entity.action_report(act_str))

	if len(report) > 0:
		viewtext += "%s.<BR />\n<BR />\n" % report

	from attr_act_view import attr_act_view
	act_view = attr_act_view()

	viewtext += '<TABLE>\n'

	from germ.attr.dummy import dummy
	for attr in entity.attr_iter('view'):
		if isinstance(attr, dummy):
			continue

		viewtext += '<TR><TH align="left">%s:</TH>' % attr.label()

		viewtext += get_cell(attr, act_view)

		viewtext += "</TR>\n"

	viewtext += "</TABLE>"

	return (viewtext, '')

def print_list(entity, act_str, page, prompt_pk_only, display_errors):
	from attr_act_view import attr_act_view
	act_view = attr_act_view()

	listtext = "<TABLE>\n"

	listtext += "\t<TR>"

	for aid in entity.attr_id_iter('view'):
		listtext += "<TH>%s</TH>" % entity.get_attr_nocheck(aid).label()

	listtext += "</TR>\n"

	for rec in entity.rsets('view'):
		listtext += "\t<TR>"

		for aid in rec.attr_id_iter('view'):
			listtext += get_cell(rec.get_attr(aid, 'view'), act_view)

		listtext += "</TR>\n"

	listtext += "</TABLE>"

	return (listtext, '')

def print_form(entity, act_str, page, prompt_pk_only, display_errors):
	import cf
	formtext = '<FORM method="GET" action="%s" autocomplete="off">\n' % \
			cf.ht_index

	# Give form again until user has seen all the fields, except for a view.
	if not prompt_pk_only or act_str == 'view':
		formtext += '<INPUT type="hidden" name="do_exec">\n'

	formtext += '<INPUT type="hidden" name="entity" value="%s">\n' % \
			entity.get_name()
	formtext += '<INPUT type="hidden" name="action" value="%s">\n' % act_str

	if page is not None:
		formtext += '<INPUT type="hidden" name="page" value="%s">\n' % page

	formtext += '<TABLE>\n'

	error_vec = []

	from attr_act_form_field import attr_act_form_field
	act_form_field = attr_act_form_field()
	from attr_act_form_key import attr_act_form_key
	act_form_key = attr_act_form_key()

	attr_vec = entity.get_attr_vec(act_str)
	pk_set = entity.get_pk_set()
	prev_was_key = False
	prev_group = None
	cnt = 0
	while len(attr_vec) > 0:
		group = entity.get_ref_group(attr_vec[0])

		from germ.error.error import error
		error(error.debug, 'printing attribute', 'aid: %s, group: %s' % \
				(attr_vec[0], group))

		if group is None:
			aid = attr_vec.pop(0)

			if prompt_pk_only:
				continue

			prev_was_key = False

			attr = entity.get_attr_nocheck(aid)

			formtext += '<TR><TD colspan="2">%s:</TD><TD>' % attr.label()

			# This can happen if the attribute is already locked for the first
			# request.
			if attr.is_locked():
				formtext += '<INPUT type="hidden" name="lock" ' \
						'value="%s">' % aid

			parm_name = cf.ht_parm_prefix_attr + aid

			act_form_field.set_parm_name(parm_name)
			attr.accept(act_form_field)

			formtext += act_form_field.get_text()

			if display_errors:
				formtext += get_error(attr, error_vec)

			formtext += '</TD></TR>\n'
		else:
			cnt += 1
			j = 0
			first = True

			# Also display remaining attributes of the same reference group.
			while j < len(attr_vec):
				if not group.has_key(attr_vec[j]):
					j += 1
					continue

				aid = attr_vec.pop(j)
				attr = entity.get_attr_nocheck(aid)

				if prompt_pk_only and aid not in pk_set:
					continue

				if prev_group != group and prev_was_key:
					formtext += '<TR><TD colspan="2"></TD><TD><HR></TD></TR>\n'
	
				prev_group = group
				prev_was_key = True

				from sets import Set as set

				keyset = group.has_fk(aid) and \
						set(group.get_keys(aid)) or set()

				locked = attr.is_locked()

				lock = locked or len(keyset) == 1

				formtext += '<TR><TD>%s:</TD><TD align="right"><INPUT ' \
						'type="radio" name="to_lock%u" ' \
						'value="%s"%s%s></TD><TD>' % \
							(attr.label(), cnt, aid,
							(lock) and ' disabled' or '',
							(not lock and first) and ' checked' or '')

				if lock:
					formtext += '<INPUT type="hidden" name="lock" ' \
							'value="%s">' % aid
				elif first:
					first = False

				parm_name = cf.ht_parm_prefix_attr + aid
				change_handler = \
						'var radios = this.form.elements[\'to_lock%u\']; ' \
						'for (var i = 0; i < radios.length; i++) {' \
						'	if (radios[i].value == \'%s\') {' \
						'		radios[i].checked = true; ' \
						'		break; ' \
						'	}' \
						'}' % \
						(cnt, aid)

				if group.has_fk(aid):
					formtext += '<SELECT name="%s" onchange="%s"%s>' % \
							(parm_name, change_handler,
							locked and ' disabled' or '')

					if attr.is_set():
						cur_key = attr.sql_str()
					else:
						cur_key = None

					tmp_attr = attr.copy()

					prev_key = None
					for key in keyset:
						formtext += '\t<OPTION value="%s"%s>' % \
								(key, key == cur_key and ' selected' or '')

						tmp_attr.set_sql(key)

						tmp_attr.accept(act_form_key)
						formtext += act_form_key.get_text()

						formtext += '</OPTION>\n'

						prev_key = key

					formtext += '</SELECT>'

					if attr.is_locked():
						formtext += '<INPUT type="hidden" name="%s" ' \
							'value="%s">' % (parm_name, attr.get())
				else:
					act_form_field.set_parm_name(parm_name)
					act_form_field.set_handler('change', change_handler)
					attr.accept(act_form_field)
					formtext += act_form_field.get_text()

				if display_errors:
					formtext += get_error(attr, error_vec)

				formtext += '</TD></TR>\n'

	from germ.lib.misc import txt_lang

	formtext += '<TR><TD colspan="2"></TD>' \
			'<TD><INPUT type="submit" value="%s"></TD>' \
			'</TR>\n' % txt_lang(entity.action_txt(act_str))

	formtext += '</TABLE>\n</FORM>'

	from germ.txt import errmsg

	errortext = len(error_vec) > 0 and \
			txt_lang(errmsg.attr_error) + ":<BR />\n" or ''

	for i, e_vec in enumerate(error_vec):
		err_str = ''
		for e in e_vec:
			err_str += "%s<BR />\n" % e

		errortext += '<SPAN style="color: red">%s</SPAN>: %s' % \
				(i+1, err_str)

	errortext += len(error_vec) > 0 and \
			"<BR />\n" or ''

	return (formtext, errortext)
