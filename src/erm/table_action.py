#
#  erm/table_action.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from germ.error.error import error
from germ.txt import errmsg

class table_action:
	def __init__(self, act_str, table, fill_table, raise_missing_lock = True,
			save_rset = False):
		self.__act_str = act_str
		self._tbl = table
		self.__fill_table = fill_table
		self.__save_rset = save_rset

		self.__raise_missing_lock = raise_missing_lock
		self._relation_class = 'relation'

	def execute(self, do_exec = True):
		# set default values
		self._set_default()

		# create reference groups
		missing_lock = self.__analyze()

		# Fill the table with existing values. For some actions, such as 'list'
		# or 'submit' this would not make any sense.
		if self.__fill_table:
			rec = self._tbl.get_rec()
			self._tbl._fill(rec, self.__act_str)

		# execute pre-action function
		self._tbl.pre(self.__act_str)

		if missing_lock and self.__raise_missing_lock:
			from germ.error.missing_lock import missing_lock
			raise missing_lock()

		if not do_exec:
			from germ.error.do_not_exec import do_not_exec
			raise do_not_exec()

		# execute SQL query
		self.__doit()

		# execute post-action function
		self._tbl.post(self.__act_str)

	def __analyze(self):
		# add primary key relation
		# TODO: fix this comment
		# NB: This has to be done _after_ the other reference groups are built
		# for the reason described in the 'pk_submit_relation' class.
		# Fortunately this is done in the entity constructor so we don't stand
		# a chance of violating this condition here.
		self._tbl.add_rel(self.__get_pk_rel())

		found_missing_lock = False

		for ref_grp in self._tbl.get_ref_group_vec():
			missing_lock, missing_pk_lock = \
					ref_grp.generate_keylist(self.__act_str)

			if missing_lock:
				# If we need the primary key, we have to prompt for PKs only.
				if self.__fill_table and missing_pk_lock:
						from germ.error.missing_pk_lock import missing_pk_lock
						raise missing_pk_lock()

				found_missing_lock = True

		return found_missing_lock

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
		raise error(error.error, errmsg.abstract_func)

	def _get_pk_cond_join(self, table, pk0):
		return [ None, None ]

	def _set_default(self):
		pass

	def __doit(self):
		query_str = self._get_sql_query()

		if query_str is None:
			return

		from germ.lib.db_iface import db_iface
		from _mysql_exceptions import ProgrammingError

		try:
			rset = db_iface.query(query_str)
		except ProgrammingError, e:
			self._tbl.create()

			rset = db_iface.query(query_str)

		if self.__save_rset:
			self._tbl.set_rset(rset)
