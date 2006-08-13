#
#  erm/tbl_act_list.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from table_action import *

class tbl_act_list(table_action):
	def __init__(self, act_str, table):
		table_action.__init__(self, act_str, table, fill_table = False,
				raise_missing_lock = False, save_rset = True)

	def _get_sql_query(self):
		name = self._tbl.get_name()
		key = self._tbl.get_attr_sql()

		if key == '':
			key = '1'

		#return "SELECT * FROM %s" % name
		return "SELECT * FROM %s WHERE %s" % (name, key)
# TODO: remove, this has already been done in fill_table
#		name = self._tbl.get_name()
#		pk = self._tbl.get_attr_sql_pk()
#
#		return "SELECT * FROM %s WHERE %s" % (name, pk)
