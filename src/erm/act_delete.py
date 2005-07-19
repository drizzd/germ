#
#  act_delete.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from action import *
from tbl_act_delete import *

class act_delete(action):
	def __init__(self, act_str):
		action.__init__(self, act_str)

	def visit_table(self, entity):
		tbl_act = tbl_act_delete(self.act_str, entity)
		tbl_act.execute()
