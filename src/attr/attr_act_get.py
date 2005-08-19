#
#  attr_act_get.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from attr_action import *

class attr_act_get(attr_action):
	def __init__(self):
		self._text = None

	def get_text(self):
		return self._text

	def visit_passwd(self, attr):
		self._text = ''

	def visit_string(self, attr):
		val = attr.get()
		if val is None:
			val = ''

		self._text = val

	def visit_int(self, attr):
		self._text = str(attr.get())

	def visit_date(self, attr):
		self._text = attr.get().strftime("%e. %b %Y")()

	def visit_bool(self, attr):
		import txt.misc

		if attr.get():
			self._text = misc.yes
		else:
			self._text = misc.no
