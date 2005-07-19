#
#  tbl_act_submit.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from table_action import *

class tbl_act_submit(table_action):
	def __init__(self, act_str, table):
		table_action.__init__(self, act_str, table)

	def get_pk_cond_join(self, table, pk0):
		return [ "%s.%s IS NULL" % (table, pk0), "LEFT" ]

	def check_pk_locks(self, tbl):
		# PK locks are not required for submit actions
		pass
