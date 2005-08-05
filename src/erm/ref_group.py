#
#  ref_group.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

class ref_group:
	""" reference groups are used to identify the relevant
	relations for a particular action on-the-fly """

	def __init__(self, rel):
		self.__joins = []
		self.__outer_joins = []
		self.__rel_map = {}
		self.__keylist = None
		self.__session = None

		self.add_rel(rel)

	def get_keylist(self, attr):
		self.__keylist(

	def has_key(self, key):
		return self.__rel_map.has_key(key)

	def has_fk(self, key):
		# key exists _and_ is not None
		return self.__rel_map.get(key) is not None

	def join_group(self, other):
		self.__joins.extend(other.__joins)
		self.__outer_joins.extend(other.__outer_joins)
		self.__rel_map.update(other.__rel_map)

	def add_rel(self, rel):
		if rel.is_outer_join():
			self.__outer_joins.append(rel)
		else:
			self.__joins.append(rel)

		# keep track of keys so we can quickly resolve
		# reference group joins
		for key in rel.get_keys():
			self.__rel_map[key] = None

	def __get_join_cond(self, rel, attr_map):
		join_cond = []
		for key in rel.get_keys():
			if self.__rel_map[key] is None:
				self.__rel_map[key] = rel.handle_unknown_key(key, attr_map,
						join_cond)
			else:
				join_cond.append("\n\t\t%s = %s" % (rel.get_colref(key),
						self.__rel_map[key].get_colref(key)))

		if len(join_cond) > 0:
			return " ON " + " AND ".join(join_cond)
		else:
			return ""

	def generate_keylist(self, act_str, session, ent):
		self.__session = session
		self.__attr_map = ent.get_attr_map()

		# generate table references

		table_ref_vec = []
		for rel in self.__joins:
			table_ref_vec.append(rel.get_table_spec() + \
				self.__get_join_cond(rel, attr_map))

		table_ref = "\n\tJOIN ".join(table_ref_vec)

		for rel in self.__outer_joins:
			table_ref += "\n\t" + rel.get_outer_join() + " JOIN " + \
				rel.get_table_spec() + \
				self.__get_join_cond(rel, attr_map)

		# generate sort order specification

		# preserve order given by entity definition
		key_vec = []
		for attr in ent.get_attr_vec():
			if self.has_fk(attr):
				key_vec.append(attr)

		sort_spec = ", ".join(key_vec)

		# generate column specification

		col_spec_vec = []
		for key in key_vec:
			rel = self.__rel_map[key]
			col_spec_vec.append("\n\t%s.%s AS %s" % \
				(rel.get_alias(), rel.get_realkey(key), key))

		col_spec = ", ".join(col_spec_vec)

		# generate search condition

		cond = []
		for rel in self.__joins + self.__outer_joins:
			cond_str = rel.get_cond(act_str)
			cond += self.__substitute_vars(cond_str)

		missing_lock = False
		to_lock_vec = []
		to_lock_cond = []
		for key in self.__rel_map.keys():
			attr = attr_map[key]
			if attr.is_locked():
				cond += ["%s = '%s'" % (self.__rel_map[key].get_colref(key),
						attr.sql_str())]
			else:
				if attr.is_to_be_locked():
					to_lock_vec += [attr]
					to_lock_cond += ["%s = '%s'" % \
							(self.__rel_map[key].get_colref(key),
							attr.sql_str())]
				missing_lock = True

		search_cond = "\n\t(" + ") AND \n\t(".join(cond) + ")"

		# execute query

		keylist = self.__query(col_spec, table_ref, search_cond + \
				" AND \n\t".join(to_lock_cond), sort_spec)

		if len(to_lock_vec) != 0:
			if len(keylist) != 0:
				# Assert key locks
				for key in to_lock_vec:
					attr_map[key].lock()
			else:
				# Possible scenario: User locks a non-relational key and in
				# combination with the locked parameters this results in an
				# empty result set.
				# So we simply tell the user this key is not available and
				# prompt for the same values again.
				for key in to_lock_vec:
					attr_map[key].invalid_key()

				keylist = self.__query(col_spec, table_ref, search_cond,
						sort_spec)

		empty_keylist = len(keylist) == 0

		# It's also possible that there are simply no valid entries available.
		# In this case the user interface should not give the possibility to
		# execute this action in the first place.
		if empty_keylist:
			if not missing_lock:
				from error.no_valid_keys import *
				raise no_valid_keys()
			else:
				# This can happen if user tampers with locked parameters or if
				# the user interface is buggy and changes locked parameters.
				from error.error import *
				from text import errmsg
				raise error(err_fail, errmsg.invalid_key)

		self.__keylist = keylist

		return missing_lock

	def __substitute_vars(self, s):
		import re
		re.sub(r'\$([A-Za-z0-9_]*)', self.__session_val, s)

	def __session_val(self, match)
		varname = match.group(1)
		if not self.__session.has_key(varname):
			# this will evaluate all comparisons to NULL, i.e. false
			return 'NULL'

		val = self.__session[varname]
		if not isinstance(val, str):
			from error.error import *
			raise error(err_fail, "Session variables for use in an " + \
					"SQL condition must be strings",
					"variable: %s, type: %s" % (varname, type(val))

		return val

	# TODO: remove
	def get_key_vec(self)
		raise error(err_fail, "use of deprecated function")
#		if self.__key_vec is None:
#			from error.error import *
#			raise error(err_fail, "Attempt to call get_key_vec before " + \
#				"generate_keylist")
#
#		return self.__key_vec

	def __query(self, col_spec, table_ref, search_cond, sort_spec):
		sql_query = "SELECT UNIQUE %s\nFROM %s\nWHERE %s\nORDER BY %s" % \
			(col_spec, table_ref, search_cond, sort_spec)

		from lib.db_iface import *

		return db_iface.query(sql_query)
