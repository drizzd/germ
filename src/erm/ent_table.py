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

		create_defs = []
		for a in self._attr_vec
			attr = _attr_map[a]

			# TODO: add REFERENCES?
			type = attr.sql_type()
			default = attr.default()

			col_def = a + ' ' + type + ' NOT NULL'
			if default is not None:
				col_def += ' DEFAULT ' + default

			create_defs.append(col_def)

		pk_def = ', '.join(self._pk_vec)
		create_defs.append(pk_def)

		create_def = ', '.join(create_defs)

		sql_query = "CREATE TABLE IF NOT EXISTS (%s)" % create_def

		db_iface.query(sql_query)

	# retrieve record specified by primary key and fill table
	def fill_pk(self):
		# in order to fill the table with values we need an entry, identified
		# by its primary key
		self._require_pk_locks()

		from lib.db_iface import *

		rset = db_iface.query("SELECT * FROM %s WHERE %s" % \
			(self._name, self.get_attr_sql_pk()))

		if len(rset) != 1:
			from error.error import *

			# TODO: Make this an invalid_key exception. This could very well
			# occur by a user 'mistake'. On the other hand, can it still occur
			# if ref_group.generate_keylist did not complain?
			raise error(err_fail, "Invalid primary key: result is empty " + \
				"or multiple result sets", "number of result sets: %s" % \
				len(rset))

		rec = rset[0]

		self._fill(rec)
