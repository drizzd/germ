#
#  erm/act_list.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from action import *
from tbl_act_list import *

class act_list(action):
	def __init__(self, do_exec = True):
		action.__init__(self, 'list', do_exec)

	def visit_table(self, entity):
		tbl_act = tbl_act_list(self._act_str, entity)
		tbl_act.execute(self._do_exec)
