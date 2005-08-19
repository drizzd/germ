#
#  ent_table.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from entity import *

class ent_table(entity):
	def __init__(
			self, attributes, primary_keys,
			relations = [], perm = {}, pre = {}, post = {}):
		entity.__init__(self, attributes, primary_keys, relations, perm)

	def accept(self, action):
		action.visit_table(self)

	# create database table
	def init(self):
		from lib.db_iface import db_iface

		create_defs = []
		for attr_id in self._attr_ids:
			attr = self._attr_map[attr_id]

			# TODO: add REFERENCES?
			sql_type = attr.sql_type()

			col_def = attr_id + ' ' + sql_type + ' NOT NULL'
			#if default is not None:
			#	col_def += ' DEFAULT %s' % default

			create_defs.append(col_def)

		pk_def = ', '.join(self._pk_set)
		create_defs.append('PRIMARY KEY (%s)' % pk_def)

		create_def = ', '.join(create_defs)

		sql_query = "CREATE TABLE IF NOT EXISTS %s (%s)" % \
				(self._name, create_def)

		db_iface.query(sql_query)

	# retrieve record specified by primary key and fill table
	def fill_pk(self):
		# in order to fill the table with values we need an entry, identified
		# by its primary key
		self._require_pk_locks()

		from lib.db_iface import db_iface

		rset = db_iface.query("SELECT * FROM %s WHERE %s" % \
			(self._name, self.get_attr_sql_pk()))

		if len(rset) != 1:
			import error

			# TODO: Make this an invalid_key exception. This could very well
			# occur by a user 'mistake'. On the other hand, can it still occur
			# if ref_group.generate_keylist did not complain?
			raise error(err_fail, "Invalid primary key: result is empty " + \
				"or multiple result sets", "number of result sets: %s" % \
				len(rset))

		rec = rset[0]

		self._fill(rec)
