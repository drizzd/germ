#
#  ref_group.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

class ref_group:
	""" reference groups are used to identify the relevant
	relations for a particular action on-the-fly """

	def __init__(self, rel, ent):
		self.__joins = []
		self.__outer_joins = []
		self.__rel_map = {}
		self.__key_map = None
		self.__ent = ent
		self.__session = ent.get_session()

		self.add_rel(rel)

	def get_keys(self, key):
		return self.__key_map[key]

	def get_rel_keys(self):
		return self.__rel_map.keys()

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

	def __get_join_cond(self, rel, act_str):
		join_cond = []
		for key in rel.get_keys():
			if self.__rel_map[key] is None:
				self.__rel_map[key] = rel.handle_unknown_key(self.__ent, key,
						act_str, join_cond)
				#from error import *
				#error(err_debug, 'handling unknown key', 'key: %s, ' \
				#		'rel_map: %s, join_cond: %s' % (key, self.__rel_map,
				#			join_cond))
			else:
				#error(err_debug, 'adding join condition', 'key: %s, ' \
				#		'rel_map: %s' % (key, self.__rel_map))
				join_cond.append("\n      %s = %s" % (rel.get_colref(key),
						self.__rel_map[key].get_colref(key)))

		if len(join_cond) > 0:
			return " ON " + " AND ".join(join_cond)
		else:
			return ""

	def get_colref(self, key, rel):
		# TODO: what was this code for???
		if rel is not None:
			return rel.get_colref(key)

		return '%s.%s' % (self.__ent.get_name(), key)

	def generate_keylist(self, act_str):
		# generate table references

		table_ref_vec = []
		for rel in self.__joins:
			table_ref_vec.append(rel.get_table_spec() + \
					self.__get_join_cond(rel, act_str))

		table_ref = "\n   JOIN ".join(table_ref_vec)

		if len(self.__joins) == 0:
			# This should only happen if there are only non-relational
			# PKs.

			# TODO: find out if this is possible and handle it appropriately
			if len(self.__outer_joins) > 1:
				from error import *
				raise error(err_warn, "No inner joins, multiple outer joins",
						'number of outer joins: %s' % len(self.__outer_joins))

			#table_ref_vec = []
			#for rel in self.__outer_joins:
			#	table_ref_vec.append(rel.get_table_spec() + \
			#			self.__get_join_cond(rel, act_str))

			#table_ref += "\n   JOIN ".join(table_ref_vec)

			table_ref = self.__outer_joins[0].get_table_spec()
		else:
			for rel in self.__outer_joins:
				table_ref += "\n   " + rel.get_outer_join() + " JOIN " + \
					rel.get_table_spec() + \
					self.__get_join_cond(rel, act_str)

		# generate search condition

		search_cond = []
		for rel in self.__joins + self.__outer_joins:
			cond_str = rel.get_cond(act_str)
			if cond_str is not None:
				search_cond.append('(%s)' % self.__substitute_vars(cond_str))

		condition = self.__ent.get_condition()
		if condition.has_key(act_str):
			search_cond.append('(%s)' % \
					self.__substitute_vars(condition[act_str]))

		missing_lock = False
		to_lock_vec = []
		lock_cond = []
		to_lock_cond = []
		for key, rel in self.__rel_map.iteritems():
			attr = self.__ent.get_attr_nocheck(key)

			if attr.is_locked():
				lock_cond.append("%s = '%s'" % (self.get_colref(key, rel),
						attr.sql_str()))
			elif attr.is_to_be_locked():
				to_lock_vec.append(key)
				to_lock_cond.append("%s = '%s'" % \
						(self.get_colref(key, rel), attr.sql_str()))
			else:
				if len(self.__joins) == 0:
					return True

				missing_lock = True

		# generate sort order specification

		# preserve order given by entity definition
		key_vec = []
		for attr in self.__ent.get_attr_ids():
			if self.has_fk(attr):
				key_vec.append(attr)

		sort_spec = ", ".join(key_vec)

		# generate column specification

		col_spec_vec = []
		for key in key_vec:
			rel = self.__rel_map[key]
			col_spec_vec.append("\n   %s AS %s" % \
				(rel.get_colref(key), key))
			#col_spec_vec.append("\n   %s.%s AS %s" % \
			#	(rel.get_alias(), rel.get_realkey(key), key))

		col_spec = ", ".join(col_spec_vec)

		#from error import *
		#error(err_debug, 'constructing search condition', 'search_cond: %s, ' \
		#		'lock_cond: %s, to_lock_cond: %s' % \
		#		(search_cond, lock_cond, to_lock_cond))

		# execute query

		res_ok, rset = self.__query_if(len(self.__joins), col_spec,
				table_ref, search_cond, lock_cond, to_lock_cond, sort_spec)

		if len(to_lock_vec) != 0:
			if res_ok:
				# Assert key locks
				for key in to_lock_vec:
					self.__ent.get_attr_nocheck(key).lock()
			else:
				# Possible scenario: User locks a non-relational key and in
				# combination with the locked parameters this results in an
				# empty result set.
				# So we simply tell the user this key is not available and
				# prompt for the same values again.
				for key in to_lock_vec:
					self.__ent.get_attr_nocheck(key).invalid_key()

				missing_lock = True

				if len(self.__joins) == 0:
					return True

				res_ok, rset = self.__query_if(len(self.__joins),
						col_spec, table_ref, search_cond, lock_cond, [],
						sort_spec)

		# It's also possible that there are simply no valid entries available.
		# In this case the user interface should not give the possibility to
		# execute this action in the first place.
		if not res_ok:
			if missing_lock:
				self.__key_map = dict(zip(key_vec, len(key_vec)*[[]]))

				from error.no_valid_keys import no_valid_keys
				raise no_valid_keys()
			else:
				# This can happen if user tampers with locked parameters or if
				# the user interface is buggy and changes locked parameters.
				from error import *
				from txt import errmsg
				raise error(err_fail, errmsg.invalid_key)

		if len(self.__joins) > 0:
			self.__key_map = dict(zip(key_vec, zip(*rset)))

		from error import *
		error(err_debug, 'keylist', 'missing_lock: %s, key_map: %s' % \
					(missing_lock, self.__key_map))

		error(err_debug, 'after keylist')

		return missing_lock

	def __substitute_vars(self, s):
		import re

		return re.sub(r'\$([A-Za-z0-9_]*)', self.__session_val, s)

	def __session_val(self, match):
		varname = match.group(1)
		if not self.__session.has_key(varname):
			# this will evaluate all comparisons to NULL, i.e. false
			return 'NULL'

		val = self.__session[varname]
		if not isinstance(val, str):
			import error
			raise error(err_fail, "Session variables for use in an " + \
					"SQL condition must be strings",
					"variable: %s, type: %s" % (varname, type(val)))

		return val

	def __query_if(self, joins_len, col_spec, table_ref, search_cond,
			lock_cond, to_lock_cond, sort_spec):
		if joins_len == 0:
			rset = self.__query('*', table_ref, lock_cond + to_lock_cond)
			res_ok = len(rset) == 0
		else:
			rset = self.__query(col_spec, table_ref,
					search_cond + lock_cond + to_lock_cond, sort_spec)
			res_ok = len(rset) != 0

		return (res_ok, rset)

	def __query(self, col_spec, table_ref, cond, sort_spec = None):
		if len(cond) == 0:
			search_str = ''
		else:
			search_str = '\nWHERE ' + ' AND\n   '.join(cond)

		if sort_spec is None:
			sort_spec_str = ''
		else:
			sort_spec_str = '\nORDER BY ' + sort_spec

		sql_query = "SELECT DISTINCT %s\nFROM %s%s%s" % \
				(col_spec, table_ref, search_str, sort_spec_str)

		from lib.db_iface import db_iface

		return db_iface.query(sql_query)
