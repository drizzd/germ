#
#  ui_ht/attr_act_form_field.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from germ.attr.attr_act_get import *

class attr_act_form_field(attr_act_get):
	def __init__(self):
		attr_act_get.__init__(self)

		self.__parm_name = None
		self.__handler = {}

	def set_parm_name(self, name):
		self.__parm_name = name

	def set_handler(self, handler, value):
		self.__handler[handler] = value

	def __get_handler_text(self):
		handler_text = ""

		for i in self.__handler.iteritems():
			handler_text += ' on%s="%s"' % i

		return handler_text

	def generic_text(self, attr, length = 10, inp_type = 'text'):
		act_get = attr_act_get()
		attr.accept(act_get)

		self._text = '<INPUT type="%s" maxlength="%s" name="%s"%s ' \
				'value="%s"%s>' % (inp_type, length, self.__parm_name,
				self.__get_handler_text(), act_get.get_text(),
				self.__lock_str(attr.is_locked()))
		if attr.is_locked():
			self._text += '<INPUT type="hidden" name="%s" ' \
				'value="%s">' % (self.__parm_name, attr.get())

		self.__parm_name = None

	def __lock_str(self, is_locked):
		return is_locked and ' disabled' or ''

	def visit_text(self, attr):
		act_get = attr_act_get()
		attr.accept(act_get)

		self._text = '<TEXTAREA name="%s"%s%s>%s</TEXTAREA>' % \
				(self.__parm_name, self.__get_handler_text(),
				self.__lock_str(attr.is_locked()), act_get.get_text())
		if attr.is_locked():
			self._text += '<INPUT type="hidden" name="%s" ' \
				'value="%s">' % (self.__parm_name, attr.get())

		self.__parm_name = None

	def visit_sql_id(self, attr):
		self.visit_int(attr)

	def visit_string(self, attr):
		self.generic_text(attr, attr.get_length())

	def visit_plain_pwd(self, attr):
		self.generic_text(attr, 16, 'password')

	def visit_passwd(self, attr):
		self.generic_text(attr, 16, 'password')

	def visit_int(self, attr):
		self.generic_text(attr)

	def visit_choice(self, attr):
		from germ.lib import misc

		self._text = '<SELECT name="%s"%s>\n' % (self.__parm_name, \
				self.__lock_str(attr.is_locked()))

		for i, choice in enumerate(attr.get_options()):
			self._text += '\t<OPTION value="%s"%s>%s</OPTION>\n' % \
					(i, i == attr.get() and ' selected' or '',
						misc.txt_lang(choice))

		self._text += "</SELECT>"

	def visit_date(self, attr):
		date = attr.get()

		input_vec = []
		for val, length in [('year', 4), ('month', 2), ('day', 2)]:
			date_val = date is None and '' or \
					('%%0%sd' % length) % getattr(date, val)

			input_vec.append('<INPUT type="text" name="%s__%s" length="%s" ' \
					'size="%s" value="%s"%s>' % \
					(self.__parm_name, val, length, length, date_val,
					self.__lock_str(attr.is_locked())))

		self._text = '-'.join(input_vec)

	def visit_bool(self, attr):
		# HTML does not specify any value if the checkbox is turned off, so we
		# set the hidden value to off. The value be overwritten by the
		# subsequent checkbox if it is indeed checked.
		self._text = '<INPUT type="hidden" name="%s" value="off">' \
				'<INPUT type="checkbox" name="%s"%s%s>' % \
				(self.__parm_name, self.__parm_name,
				attr.get() and ' checked' or '',
				self.__lock_str(attr.is_locked()))
