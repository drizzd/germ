#
#  tbl_act_submit.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from table_action import *

class tbl_act_submit(table_action):
	def __init__(self, act_str, table):
		table_action.__init__(self, act_str, table, require_pk_locks = False)

	def _get_pk_cond_join(self, table, pk0):
		return [ "%s.%s IS NULL" % (table, pk0), "LEFT" ]

	def _get_sql_query(self, table):
		name = table.get_name()
		attr = table.get_attr_sql()

		sql_query = "INSERT INTO %s SET %s" % (name, attr)

		return sql_query
