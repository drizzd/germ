#
#  tbl_act_delete.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from table_action import *

class tbl_act_delete(table_action):
	def __init__(self, act_str, table):
		table_action.__init__(self, act_str, table, require_pk_locks = True)

	def get_pk_cond_join(self, table, pk0):
		return [ None, None ]

	def _get_sql_query(self, table, sql_str, sql_str_pk):
		name = table.get_name()
		pk = table.get_attr_sql_pk()

		return "DELETE FROM %s WHERE %s" % (name, pk)
