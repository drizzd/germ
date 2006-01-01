#
#  erm/ent_table.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from entity import *

class ent_table(entity):
	from germ.txt import misc

	def __init__(self, attributes, primary_keys, relations = [],
			condition = {}, item_txt = {}, action_txt = misc.action,
			action_report = misc.action_report, perm = {}, pre = {},
			post = {}, magic_var = {}):
		entity.__init__(self, attributes, primary_keys, relations, condition,
				item_txt, action_txt, action_report, perm, pre, post,
				magic_var)

	def do_accept(self, action):
		action.visit_table(self)

	# create database table
	def create(self):
		from germ.lib.db_iface import db_iface

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

		#sql_query = "CREATE TABLE IF NOT EXISTS %s (%s)" % \
		sql_query = "CREATE TABLE %s (%s)" % \
				(self._name, create_def)

		db_iface.query(sql_query)

	# retrieve record specified by primary key and fill table
	def fill_pk(self):
		# in order to fill the table with values we need an entry, identified
		# by its primary key
		if not self.pks_locked():
			from germ.error.missing_pk_lock import missing_pk_lock
			raise missing_pk_lock()

		from germ.lib.db_iface import db_iface

		rset = db_iface.query("SELECT * FROM %s WHERE %s" % \
			(self._name, self.get_attr_sql_pk()))

		if len(rset) != 1:
			# TODO: Make this an invalid_key exception. This could very well
			# occur by a user 'mistake'. On the other hand, can it still occur
			# if ref_group.generate_keylist did not complain?
			from germ.error.error import error
			raise error(error.fail, "Invalid primary key: result is empty " + \
					"or has multiple records", "number of records: %s" % \
					len(rset))

		rec = rset[0]

		self._fill(rec)
