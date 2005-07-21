#
#  relation.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

class relation:
	def __init__(
			self, table, keys,
			alias = None, cond = None, outer_join = None):
		self.__table = table
		self.__alias = alias
		self.__cond = cond
		self.__fk_map = keys
		self.__outer_join = outer_join

	def get_cond(self, act_str):
		if self.__cond.has_key(act_str):
			return [self.__cond[act_str]]
		else:
			return []

	def is_outer_join(self):
		return self.__outer_join is not None

	def get_outer_join(self):
		return self.__outer_join

	def get_alias(self):
		if self.__alias is not None:
			return self.__alias
		else:
			return self.__table

	def has_alias(self):
		return self.__alias is not None

	def get_table(self):
		return self.__table

	def get_table_spec(self):
		table_spec = self.__table
		if self.__alias is not None:
			table_spec += " AS " + self.__alias

		return table_spec

	def get_keys(self):
		return self.__fk_map.keys()

	def get_realkey(self, key):
		return self.__fk_map[key]

	def get_colref(self, key):
		return "%s.%s" % (self.get_alias(), self.get_realkey(key))

	def get_join_cond(self, rel_map, attr_map, lock_map):
		join_cond = []
		for key in self.get_keys():
			if rel_map[key] is None:
				self.handle_unknown_key(
					key, rel_map, attr_map, lock_map, join_cond)
			else:
				join_cond.append("\n\t\t%s = %s" %
					(self.get_colref(key), rel_map[key].get_colref(key)))

		if len(join_cond) > 0:
			return " ON " + " AND ".join(join_cond)
		else:
			return ""

	def handle_unknown_key(self, key, rel_map, attr_map, lock_map, join_cond):
		rel_map[key] = self
