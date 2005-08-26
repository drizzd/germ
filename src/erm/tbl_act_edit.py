#
#  erm/tbl_act_edit.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from table_action import *

class tbl_act_edit(table_action):
	def __init__(self, act_str, table):
		table_action.__init__(self, act_str, table, fill_table = True)

	def _get_sql_query(self):
		name = self._tbl.get_name()
		attr = self._tbl.get_attr_sql_nopk()
		pk = self._tbl.get_attr_sql_pk()

		return "UPDATE %s SET %s WHERE %s" % (name, attr, pk)
