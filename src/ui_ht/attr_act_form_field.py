#
#  attr_act_form_field.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from attr.attr_act_get import *

class attr_act_form_field(attr_act_get):
	def __init__(self):
		attr_act_get.__init__(self)

		self.__parm_name = None

	def set_parm_name(self, name):
		self.__parm_name = name

	def generic_text(self, attr, length = 10, inp_type = 'text'):
		attr_act_get.accept(self, attr)
		text = self._text

		self._formtext = '<INPUT type="%s" maxlength="%s" name="%s" ' \
				'value="%s"%s>' % (inp_type, length, self.__parm_name,
				val, self.__lock_str(attr.is_locked()))

		self.__parm_name = None

	def __lock_str(self, is_locked):
		return is_locked and ' disabled' or ''

	def visit_string(self, attr):
		self.generic_text(attr, attr.get_length())

	def visit_passwd(self, attr):
		self.generic_text(attr, 16, 'password')

	def visit_int(self, attr):
		self.generic_text(attr)

	def visit_choice(self, attr):
		import cf

		self._formtext = '<SELECT name="%s"%s>\n' % (self.__parm_name, \
				self.__lock_str(attr.is_locked()))

		for i, choice in enumerate(attr.get_options()):
			self._formtext += '\t<OPTION value="%s"%s>%s</OPTION>\n' % \
					(i, i == attr.get() and ' selected' or '',
						choice.get(cf.lang, choice['en']))

		self._formtext += "</SELECT>"

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

		self._formtext = '-'.join(input_vec)

	def visit_bool(self, attr):
		self._formtext = '<INPUT type="checkbox" name="%s"%s%s>' % \
				(self.__parm_name, attr.get() and ' checked' or '',
					self.__lock_str(attr.is_locked()))
