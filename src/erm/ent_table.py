#
#  ent_table.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from entity import *

class ent_table(entity):
	def __init__(
			self, name, attributes, primary_keys,
			relations = [], perm = {}, pre = {}, post = {}):
		entity.__init__(self, name, attributes, primary_keys, relations, perm)

	def accept(self, action):
		action.visit_table(self)

	# create database table
	def init(self):
		from lib.db_iface import *
		import string

		create_defs = []
		for a in self._attr_vec
			attr = __attr_map[a]

			# TODO: add REFERENCES?
			type = attr.sql_type()
			default = attr.default()

			col_def = a + ' ' + type + ' NOT NULL'
			if default is not None:
				col_def += ' DEFAULT ' + default

			create_defs.append(col_def)

		pk_def = string.join(self._pk_vec, ', ')
		create_defs.append(pk_def)

		create_def = string.join(create_defs, ', ')

		sql_query = "CREATE TABLE IF NOT EXISTS " + create_def

		db_iface.query(sql_query)
