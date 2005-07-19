#
#  pk_relation.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from relation import *

class pk_relation(relation):
	def __init__(
			self, table, keys,
			alias = None, cond = None, outer_join = None):
		relation.__init__(self, table, keys, alias, cond, outer_join)

	def handle_unknown_key(self, key, rel_map, attr_map, join_cond):
		from missing_parm import *

		attr = attr_map[key]

		attr.require_lock()
		if not attr.is_locked():
			raise missing_parm()

		join_cond.append("\n\t\t%s = %s" %
			(self.get_colref(key), attr_map[key].sql_str()))
