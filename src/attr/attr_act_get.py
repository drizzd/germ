#
#  attr_act_get.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from attr_action import *

class attr_act_get(attr_action):
	def __init__(self):
		self.value = None

	def visit_string(attr):
		self.value = attr.get()

	def visit_int(attr):
		self.value = str(attr.get())

	def visit_date(attr):
		self.value = attr.get().strftime("%e. %b %Y")()

	def visit_bool(attr):
		import text.misc

		if attr.get():
			self.value = misc.yes
		else:
			self.value = misc.no
