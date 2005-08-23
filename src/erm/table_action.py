#
#  table_action.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from error.error import *
from txt import errmsg

class table_action:
	def __init__(self, act_str, table, fill_table, save_rset = False):
		self.__act_str = act_str
		self._tbl = table
		self.__fill_table = fill_table
		self.__save_rset = save_rset

		self._relation_class = 'relation'

	def execute(self, do_exec = True):
		# set default values
		self._set_default()

		# create reference groups
		missing_lock = self.__analyze()

		# Fill the table with existing values. For some actions, such as 'list'
		# or 'submit' this would not make any sense.
		if self.__fill_table:
			self._tbl.fill_pk()

		if missing_lock:
			from error.missing_lock import missing_lock
			raise missing_lock()

		error(err_debug, '-> do execute', str(do_exec))

		if not do_exec:
			from error.do_not_exec import do_not_exec
			raise do_not_exec()

		# execute pre-action function
		self._tbl.pre(self.__act_str)

		# execute SQL query
		self.__doit()

		# execute post-action function
		self._tbl.post(self.__act_str)

	def __analyze(self):
		# add primary key relation
		# NB: This has to be done _after_ the other reference groups are built
		# for the reason described in the 'pk_submit_relation' class.
		# Fortunately this is done in the entity constructor so we don't stand
		# a chance of violating this condition here.
		self._tbl.add_rel(self.__get_pk_rel())

		missing_lock = False

		for ref_grp in self._tbl.get_ref_group_vec():
			if ref_grp.generate_keylist(self.__act_str):
				# If we need the primary key, we have to prompt for PKs only.
				if self.__fill_table:
					pk0 = self._tbl.get_pk_set().copy().pop()

					if ref_grp.has_key(pk0):
						from error.missing_pk_lock import missing_pk_lock
						raise missing_pk_lock()

				missing_lock = True

		return missing_lock

	def __get_pk_rel(self):
		pk_set = self._tbl.get_pk_set()
		table = self._tbl.get_name()
		cond, outer_join = self._get_pk_cond_join(table, pk_set.copy().pop())

		rel_cls = eval("__import__('%s', globals(), locals(), ['%s']).%s" % \
				(3*(self._relation_class,)))

		return rel_cls(
			table = table,
			keys = dict(zip(pk_set, pk_set)),
			cond = cond is None and {} or { self.__act_str: cond },
			outer_join = outer_join)

	def _get_sql_query(self, table, sql_str):
		raise error(err_error, errmsg.abstract_func)

	def _get_pk_cond_join(self, table, pk0):
		return [ None, None ]

	def _set_default(self):
		pass

	def __doit(self):
		sql_query = self._get_sql_query()

		if sql_query is None:
			return

		from lib.db_iface import *
		rset = db_iface.query(sql_query)

		if self.__save_rset:
			self._tbl.set_rset(rset)
