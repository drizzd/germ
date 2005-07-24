#
#  attr_action.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from lib.error import *
import text.errmsg

class attr_action:
	def __init__(self):
		raise error(err_fail, errmsg.abstract_inst)

	def visit_string(attr):
		raise error(err_fail, errmsg.unimplemented)

	def visit_choice(attr):
		raise error(err_fail, errmsg.unimplemented)

	def visit_time(attr):
		raise error(err_fail, errmsg.unimplemented)

	def visit_date(attr):
		raise error(err_fail, errmsg.unimplemented)
