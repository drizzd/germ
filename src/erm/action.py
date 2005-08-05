#
#  action.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from error.error import *
from text import errmsg

class action:
	def __init__(self, act_str, session, do_exec):
		self._act_str = act_str
		self._session = session
		self._do_exec = do_exec

	def visit_table(self, entity):
		raise error(err_fail, errmsg.unimplemented)

	def visit_view(self, entity):
		raise error(err_fail, errmsg.unimplemented)

	def visit_virtual(self, entity):
		raise error(err_fail, errmsg.unimplemented)
