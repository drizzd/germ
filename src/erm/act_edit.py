#
#  act_edit.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from action import *
from tbl_act_edit import *

class act_edit(action):
	def __init__(self, do_exec = True):
		action.__init__(self, 'edit', do_exec)

	def visit_table(self, entity):
		tbl_act = tbl_act_edit(self._act_str, entity)
		tbl_act.execute(self._do_exec)

	def visit_virtual(self, entity):
		entity.edit(self._act_str, self._do_exec)
