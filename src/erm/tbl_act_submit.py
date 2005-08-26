#
#  erm/tbl_act_submit.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from table_action import *

class tbl_act_submit(table_action):
	def __init__(self, act_str, table):
		table_action.__init__(self, act_str, table,
				fill_table = False)
		self._relation_class = 'pk_submit_relation'

	def _set_default(self):
		self._tbl.set_default()

	def _get_pk_cond_join(self, table, pk0):
		return [ "%s.%s IS NULL" % (table, pk0), "LEFT" ]

	def _get_sql_query(self):
		name = self._tbl.get_name()
		attr = self._tbl.get_attr_sql()

		sql_query = "INSERT INTO %s SET %s" % (name, attr)

		return sql_query
