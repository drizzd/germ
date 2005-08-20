#
#  tbl_act_delete.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from table_action import *

class tbl_act_delete(table_action):
	def __init__(self, act_str, table):
		table_action.__init__(self, act_str, table, fill_table = True)

	def _get_sql_query(self):
		name = self._tbl.get_name()
		pk = self._tbl.get_attr_sql_pk()

		return "DELETE FROM %s WHERE %s" % (name, pk)
