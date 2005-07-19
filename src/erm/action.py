#
#  action.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from lib.error import *
import text.errmsg

class action:
	def __init__(self, act_str):
		self.act_str = act_str

	def visit_table(self, entity):
		raise error(err_fail, errmsg.unimplemented)

	def visit_view(self, entity):
		raise error(err_fail, errmsg.unimplemented)

	def visit_virtual(self, entity):
		raise error(err_fail, errmsg.unimplemented)
