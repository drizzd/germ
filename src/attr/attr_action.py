#
#  attr/attr_action.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from germ.error.error import error
from germ.txt import errmsg

class attr_action:
	def __init__(self):
		raise error(error.fail, errmsg.abstract_inst)

	def visit_sql_id(self, attr):
		raise error(error.fail, errmsg.unimplemented)

	def visit_text(self, attr):
		raise error(error.fail, errmsg.unimplemented)

	def visit_dummy(self, attr):
		raise error(error.fail, errmsg.unimplemented)

	def visit_string(self, attr):
		raise error(error.fail, errmsg.unimplemented)

	def visit_int(self, attr):
		raise error(error.fail, errmsg.unimplemented)

	def visit_choice(self, attr):
		raise error(error.fail, errmsg.unimplemented)

	def visit_time(self, attr):
		raise error(error.fail, errmsg.unimplemented)

	def visit_date(self, attr):
		raise error(error.fail, errmsg.unimplemented)

	def visit_bool(self, attr):
		raise error(error.fail, errmsg.unimplemented)
