#
#  ref_group.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from lib.db_iface import *

class ref_group:
	""" reference groups are used to identify the relevant relations for a
	particular action on-the-fly """

	def __init__(self, rel):
		self.__joins = []
		self.__outer_joins = []
		self.__rel_map = {}
		self.__fk_vec = None
		self.__keylist = None

		self.add_rel(rel)

	def has_key(self, key):
		return self.__rel_map.has_key(key)

	def join_group(self, other):
		self.__joins.extend(other.__joins)
		self.__outer_joins.extend(other.__outer_joins)
		self.__rel_map.update(other.__rel_map)

	def add_rel(self, rel):
		if rel.is_outer_join():
			self.__outer_joins.append(rel)
		else:
			self.__joins.append(rel)

		for key in rel.get_keys():
			if not self.__rel_map.has_key(key):
				self.__rel_map[key] = None

	def generate_keylist(self, act_str, attr_vec, attr_map, lock_map):
		import string

		# generate table references

		table_ref_vec = []
		for rel in self.__joins:
			table_ref_vec.append(
				rel.get_table_spec() +
				rel.get_join_cond(self.__rel_map, attr_map, lock_map))
		table_ref = string.join(table_ref_vec, "\n\tJOIN ")

		for rel in self.__outer_joins:
			table_ref += \
				"\n\t" + rel.get_outer_join() + " JOIN " + \
				rel.get_table_spec() + \
				rel.get_join_cond(self.__rel_map, attr_map, lock_map)

		# generate sort order specification

		self.__fk_vec = []
		for attr in attr_vec:
			if self.__rel_map.has_key(attr):
				self.__fk_vec.append(attr)

		sort_spec = string.join(self.__fk_vec, ", ")

		# generate column specification

		col_spec_vec = []
		for key in self.__fk_vec:
			rel = self.__rel_map[key]
			col_spec_vec.append(
				"\n\t%s.%s AS %s" %
				(rel.get_alias(), rel.get_realkey(key), key))
		col_spec = string.join(col_spec_vec, ", ")

		# generate search condition

		cond = []
		for rel in self.__joins + self.__outer_joins:
			cond += rel.get_cond(act_str)

		for key in self.__fk_vec:
			attr = attr_map[key]
			if attr.is_locked():
				cond += \
					["%s = '%s'" % \
					(self.__rel_map[key].get_colref(key), attr.sql_str())]

		search_cond = "\n\t(" + string.join(cond, ") AND \n\t(") + ")"

		sql_query = \
			"SELECT %s \nFROM %s \nWHERE %s \nORDER BY %s" % \
			(col_spec, table_ref, search_cond, sort_spec)

		print sql_query
#		self.__keylist = db_iface.query(sql_query)
