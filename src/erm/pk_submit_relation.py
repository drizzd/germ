#
#  pk_submit_relation.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from relation import *

class pk_submit_relation(relation):
	def __init__(
			self, table, keys,
			alias = None, cond = None, outer_join = None):
		relation.__init__(self, table, keys, alias, cond, outer_join)

	def handle_unknown_key(self, key, rel_map, attr_map, lock_map, join_cond):
		from missing_parm import *

		attr = attr_map[key]

		if not attr.is_locked():
			lock_map[key] = None
			raise missing_parm()

		join_cond.append("\n\t\t%s = %s" %
			(self.get_colref(key), attr_map[key].sql_str()))
