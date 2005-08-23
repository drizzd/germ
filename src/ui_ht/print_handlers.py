#
#  print_handlers.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

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

def print_view(entity, act_str, prompt_pk_only):
	viewtext = ''

	from lib.misc import txt_lang
	from txt.misc import action_report

	report = txt_lang(entity.action_report(act_str))

	if len(report) > 0:
		viewtext += "%s.<BR />\n<BR />\n" % report

	from attr_act_view import attr_act_view
	act_view = attr_act_view()

	viewtext += '<TABLE>\n'

	for attr in entity.attr_iter('view'):
		viewtext += '<TR><TH align="left">%s:</TH>' % attr.label()

		viewtext += get_cell(attr, act_view)

		viewtext += "</TR>\n"

	viewtext += "</TABLE>"

	return viewtext

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
	formtext = '<FORM method="GET" action="%s" autocomplete="off">\n' % \
			('/' + cf.ht_path + '/' + cf.ht_index)

	# give form again until user has seen all the fields, except for a view
	if not prompt_pk_only or act_str == 'view':
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
	prev_was_key = False
	prev_group = None
	cnt = 0
	while len(attr_vec) > 0:
		from error.error import error
		error(error.debug, 'getting reference group')

		group = entity.get_ref_group(attr_vec[0])

		from error.error import error
		error(error.debug, 'got reference group', 'group: %s' % group)

		if group is None:
			aid = attr_vec.pop(0)

			if prompt_pk_only:
				continue

			prev_was_key = False

			attr = entity.get_attr_nocheck(aid)

			formtext += '<TR><TD colspan="2">%s:</TD><TD>' % attr.label()

			parm_name = cf.ht_parm_prefix_attr + aid

			from error.error import error
			error(error.debug, 'printing attribute form element', 'aid: %s' % aid)

			act_form_field.set_parm_name(parm_name)
			attr.accept(act_form_field)

			formtext += act_form_field.get_text()

			formtext += get_error(attr, error_vec)

			formtext += '</TD></TR>\n'

			from error.error import error
			error(error.debug, 'printed attribute form element', 'aid: %s' % aid)

		else:
			cnt += 1
			j = 0
			first = True

			# also display remaining attributes of the same reference
			# group
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

				from error.error import error
				error(error.debug, 'printing key form element', 'aid: %s' % aid)

				locked = attr.is_locked()

				formtext += '<TR><TD>%s:</TD><TD align="right"><INPUT ' \
						'type="radio" name="to_lock%u" value="%s"%s%s>' \
						'</TD><TD>' % \
							(attr.label(), cnt, aid,
							locked and ' disabled' or '',
							(not locked and first) and ' checked' or '')
				if locked:
					formtext += '<INPUT type="hidden" name="lock" ' \
							'value="%s">' % aid
				elif first:
					first = False

				parm_name = cf.ht_parm_prefix_attr + aid

				if group.has_fk(aid):
					formtext += '<SELECT name="%s"%s>' % (parm_name,
							locked and ' disabled' or '')

					cur_key = attr.sql_str()

					tmp_attr = attr.copy()

					prev_key = None
					for key in group.get_keys(aid):
						if key == prev_key:
							continue

						formtext += '\t<OPTION value="%s"%s>' % \
								(key, key == cur_key and ' selected' or '')

						tmp_attr.set_sql(key)

						tmp_attr.accept(act_form_key)
						formtext += act_form_key.get_text()

						formtext += '</OPTION>\n'

						prev_key = key

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

			from error.error import error
			error(error.debug, 'leaving reference group')

	from lib.misc import txt_lang

	formtext += '<TR><TD colspan="2"></TD>' \
			'<TD><INPUT type="submit" value="%s"></TD>' \
			'</TR>\n' % txt_lang(entity.action_txt(act_str))

	formtext += '</TABLE>\n</FORM>'

	from txt import errmsg

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

	from error.error import error
	error(error.debug, 'done printing')

	return errortext + formtext
