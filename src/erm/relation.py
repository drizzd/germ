#
#  erm/relation.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

class relation:
	def __init__(self, table, keys, alias = None, cond = {},
			outer_join = None):
		self.__table = table
		self.__alias = alias
		self.__cond = cond
		self.__fk_map = keys
		self.__outer_join = outer_join

		self.__missing_lock = False
		self.__to_be_locked = False

	def missing_lock(self):
		self.__missing_lock = True

	def to_lock(self):
		self.__to_be_locked = True

	def is_to_be_locked(self):
		return self.__to_be_locked

	def get_cond(self, act_str):
		if self.__missing_lock:
			return None

		from germ.lib import misc

		return misc.get_cond(self.__cond, act_str)

	def is_outer_join(self):
		return self.__outer_join is not None

	def get_outer_join(self):
		return self.__outer_join

	def get_table(self):
		return self.__table

	def get_alias(self):
		return self.__alias is None and self.__table or self.__alias

	def has_alias(self):
		return self.__alias is not None

# TODO: remove
#	def get_table(self):
#		return self.__table

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
