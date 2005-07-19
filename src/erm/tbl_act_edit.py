#
#  tbl_act_edit.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from table_action import *

class tbl_act_edit(table_action):
	def __init__(self, act_str, table):
		table_action.__init__(self, act_str, table)

	def get_pk_cond_join(self, table, pk0):
		return [ None, None ]

	def check_pk_locks(self, tbl):
		tbl.require_pk_locks(key)
