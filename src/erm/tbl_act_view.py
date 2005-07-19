#
#  tbl_act_view.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from table_action import *

class tbl_act_view(table_action):
	def __init__(self, act_str, table):
		table_action.__init__(self, act_str, table)
