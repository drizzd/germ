#
#  attr/attr_act_get.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from attr_action import *

class attr_act_get(attr_action):
	def __init__(self):
		self._text = None

	def get_text(self):
		return self._text

	def visit_plain_pwd(self, attr):
		self._text = ''

	def visit_passwd(self, attr):
		self._text = ''

	def visit_choice(self, attr):
		self._text = str(attr)

	def visit_string(self, attr):
		val = attr.get()
		if val is None:
			val = ''

		self._text = val

	def visit_int(self, attr):
		self._text = str(attr.get())

	def visit_date(self, attr):
		from germ.lib import misc

		self._text = misc.date_str_nice(attr.get())

	def visit_bool(self, attr):
		import germ.txt.misc

		if attr.get():
			self._text = misc.yes
		else:
			self._text = misc.no

	def visit_dummy(self, attr):
		self._text = ''
