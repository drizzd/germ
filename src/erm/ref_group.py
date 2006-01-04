#
#  erm/ref_group.py
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
		# key exists _and_ is not a pk_submit_relation
		rel = self.__rel_map.get(key)

		return rel is not None and not rel.is_outer_join()

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

	def __get_join_cond(self, rel):
		join_cond = []
		for key in rel.get_keys():
			colref = None

			other_rel = self.__rel_map.get(key)
			if other_rel is None:
				self.__rel_map[key] = rel
				
				if rel.is_outer_join():
					# Here we check if the key is locked. We always add the
					# outer join relations to the reference groups last. Thus
					# all other relations will be evaluated first and the key
					# would already point to another relation, if another
					# relation for this key existed.
					attr = self.__ent.get_attr_nocheck(key)

					if attr.is_locked() or attr.is_to_be_locked():
						# exclude all matches for this key (this condition is
						# used in a LEFT JOIN ... WHERE pk0 IS NULL)

						# TODO: move this to the search condition string.
						# Immediate values in the join condition are not
						# supported by all SQL databases
						colref = "'%s'" % attr.sql_str()

						if attr.is_to_be_locked():
							rel.to_lock()
					else:
						# TODO: missing lock, prevent use of search condition
						# for this relation
						rel.missing_lock()

				#from germ.error.error import error
				#error(error.debug, 'handling unknown key', 'key: %s, ' \
				#		'rel_map: %s, join_cond: %s' % (key, self.__rel_map,
				#			join_cond))
			else:
				#from germ.error.error import error
				#error(error.debug, 'adding join condition', 'key: %s, ' \
				#		'rel_map: %s' % (key, self.__rel_map))

				colref = other_rel.get_colref(key)

			if colref is not None:
				join_cond.append("\n      %s = %s" % (rel.get_colref(key),
						colref))

		if len(join_cond) > 0:
			return " ON " + " AND ".join(join_cond)
		else:
			return ""

	#def get_colref(self, key):
	#	# TODO: what was this code for???
	#	if rel is not None:
	#		return rel.get_colref(key)

	#	return '%s.%s' % (self.__ent.get_name(), key)

	def generate_keylist(self, act_str):
		# generate table references

		table_ref_vec = []
		for rel in self.__joins:
			table_ref_vec.append(rel.get_table_spec() + \
					self.__get_join_cond(rel))

		table_ref = "\n   JOIN ".join(table_ref_vec)

		if len(self.__joins) == 0:
			# This should only happen if there are only non-relational
			# PKs.

			# TODO: find out if this is possible and handle it appropriately
			if len(self.__outer_joins) > 1:
				from germ.error.error import error
				raise error(error.warn, "No inner joins, multiple outer joins",
						'number of outer joins: %s' % len(self.__outer_joins))

			#table_ref_vec = []
			#for rel in self.__outer_joins:
			#	table_ref_vec.append(rel.get_table_spec() + \
			#			self.__get_join_cond(rel))

			#table_ref += "\n   JOIN ".join(table_ref_vec)

			rel = self.__outer_joins[0]

			# make sure the relation is registerated in the rel_map, but
			# discard the join condition
			self.__get_join_cond(rel)

			table_ref = rel.get_table_spec()
		else:
			for rel in self.__outer_joins:
				table_ref += "\n   " + rel.get_outer_join() + " JOIN " + \
					rel.get_table_spec() + \
					self.__get_join_cond(rel)

		# generate search condition

		missing_lock = False
		missing_pk_lock = False
		pk_set = self.__ent.get_pk_set()
		#non_rel_missing_lock = False
		lock_cond = []
		to_lock_cond = []
		to_lock_vec = []
		for key, rel in self.__rel_map.iteritems():
			#from germ.error.error import error
			#error(error.debug, 'getting lock condition', 'key: %s, rel: %s' \
			#		% (key, rel))

			attr = self.__ent.get_attr_nocheck(key)

			if attr.is_locked():
				# TODO: pk_submit_relation should probably do something
				# different
				if not rel.is_outer_join() or len(self.__joins) == 0:
					lock_cond.append("%s = '%s'" % (rel.get_colref(key),
							attr.sql_str()))
			elif attr.is_to_be_locked():
				to_lock_vec.append(key)

				if not rel.is_outer_join() or len(self.__joins) == 0:
					to_lock_cond.append("%s = '%s'" % \
							(rel.get_colref(key), attr.sql_str()))
			else:
				if attr.perm(act_str):
					missing_lock = True

				if key in pk_set:
					missing_lock = missing_pk_lock = True

				if len(self.__joins) == 0:
					return (missing_lock, missing_pk_lock)

				#if rel.is_outer_join():
				#	non_rel_missing_lock = True

		search_cond = []
		to_lock_search_cond = []
		for rel in self.__joins + self.__outer_joins:
			cond_str = rel.get_cond(act_str)

			if cond_str is None:
				continue

			cond_str = '(%s)' % self.__substitute_vars(cond_str)

			# TODO: think about this
			# this makes sure a check for uniqueness does not collide with the
			# entry itself
			if rel.get_table() == self.__ent.get_name():
				if self.__ent.pks_locked():
					cond_str = '(%s OR (%s))' % (cond_str,
							self.__ent.get_attr_sql_pk_alias(rel.get_alias()))
#			if act_str == 'edit' and rel.is_outer_join() and \
#					rel.get_table() == self.__ent.get_name():
#				if not self.__ent.pks_locked():
#					continue
#
#				cond_str = '(%s OR (%s))' % (cond_str,
#						self.__ent.get_attr_sql_pk_alias(rel.get_alias()))

			if len(self.__joins) == 0:
				cond_str = 'NOT ' + cond_str

			if rel.is_to_be_locked():
				# If we fail, simply omit the to_lock_search_cond in the
				# second query. This is a nasty trick that will allow us to
				# get our reference keys even though the join condition is
				# wrong. This will only work if the user interface behaves
				# nicely. If both the non-relational and the relational
				# keys are wrong, we have a problem (because invalid
				# relational keys will be conceived as correct)
				#
				# Or no? Maybe this is not such a nasty trick after all.
				# The outer joins are easily controlled by the search
				# condition. Omitting it will have the same effect as if we
				# had not supplied the outer join at all. An outer join
				# will never give additional results. There can only be
				# fewer if the IS NULL condition is used.
				to_lock_search_cond.append(cond_str)
			else:
				search_cond.append(cond_str)

		condition = self.__ent.get_condition(act_str)
		if condition is not None:
			search_cond.append('(%s)' % self.__substitute_vars(condition))

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

		#from germ.error.error import error
		#error(error.debug, 'constructing search condition', 'search_cond: %s, ' \
		#		'lock_cond: %s, to_lock_cond: %s' % \
		#		(search_cond, lock_cond, to_lock_cond))

		# execute query

		res_ok, rset = self.__query_if(len(self.__joins), col_spec,
				table_ref, search_cond + to_lock_search_cond + lock_cond + \
				to_lock_cond, sort_spec)

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

					if key in pk_set:
						missing_pk_lock = True

				missing_lock = True

				if len(self.__joins) == 0:
					return (missing_lock, missing_pk_lock)

				res_ok, rset = self.__query_if(len(self.__joins),
						col_spec, table_ref, search_cond + lock_cond,
						sort_spec)

		# It's also possible that there are simply no valid entries available.
		# In this case the user interface should not give the possibility to
		# execute this action in the first place.
		if not res_ok:
			if missing_lock:
				pass
				#self.__key_map = dict(zip(key_vec, len(key_vec)*[[]]))
			else:
				# ???
				# This can happen if user tampers with locked parameters or if
				# the user interface is buggy and changes locked parameters.
				from germ.error.error import error
				from germ.txt import errmsg
				raise error(error.fail, errmsg.invalid_key, 'entity: %s, ' \
						'action: %s, res_ok: %s, missing_lock: %s' % \
						(self.__ent.get_name(), act_str,
						res_ok, missing_lock))

			from germ.error.no_valid_keys import no_valid_keys
			raise no_valid_keys()

		if len(self.__joins) > 0:
			self.__key_map = dict(zip(key_vec, zip(*rset)))

		return (missing_lock, missing_pk_lock)

	def __substitute_vars(self, s):
		import re

		return re.sub(r'\$([A-Za-z_][A-Za-z0-9_]*)(\.[A-Za-z_][A-Za-z0-9_]*)?',
				self.__session_val, s)

	def __session_val(self, match):
		if match.group(2) is not None:
			varname = match.group(2)[1:]
			ent_str = match.group(1)

			from helper import get_entity
			entity = get_entity(ent_str, self.__session,
					self.__ent.get_globals())

			val = entity.magic_var(varname)
			if val is None:
				from germ.error.error import error
				raise error(error.error, 'Invalid magic variable',
						'entity: %s, varname: %s' % (ent_str, varname))

			return str(val)

		varname = match.group(1)

		val = self.__ent.magic_var(varname)
		if val is not None:
			return val

		if not self.__session.has_key(varname):
			# this will evaluate all comparisons to NULL, i.e. false
			return 'NULL'

		val = self.__session[varname]
		if not isinstance(val, str):
			from germ.error.error import error
			raise error(error.fail, "Session variables for use in an " \
					"SQL condition must be strings",
					"variable: %s, type: %s" % (varname, type(val)))

		from germ.lib.db_iface import db_iface

		return "'%s'" % db_iface.escape_string(val)

	def __query_if(self, joins_len, col_spec, table_ref, search_cond, sort_spec):
		if joins_len == 0:
			rset = self.__query('*', table_ref, search_cond)
			res_ok = len(rset) == 0
		else:
			rset = self.__query(col_spec, table_ref,
					search_cond, sort_spec)
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

		sql_str = "SELECT DISTINCT %s\nFROM %s%s%s" % \
				(col_spec, table_ref, search_str, sort_spec_str)

		from germ.erm.helper import sql_query
		res = sql_query(sql_str, self.__session, self.__ent.get_globals())

		return res
