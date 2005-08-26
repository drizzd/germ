#
#  erm/tbl_act_view.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from table_action import *

class tbl_act_view(table_action):
	def __init__(self, act_str, table):
		table_action.__init__(self, act_str, table, fill_table = True,
				raise_missing_lock = False)

	def _get_sql_query(self):
		return None
# TODO: remove, this has already been done in fill_table
#		name = self._tbl.get_name()
#		pk = self._tbl.get_attr_sql_pk()
#
#		return "SELECT * FROM %s WHERE %s" % (name, pk)
