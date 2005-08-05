#
#  table_action.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from error.error import *
from text import errmsg

class table_action:
	def __init__(self, act_str, session, table, fill_table, save_rset = False):
		self.__act_str = act_str
		self.__session = session
		self._tbl = table
		self.__fill_table = fill_table
		self.__save_rset = save_rset

		self._relation_class = 'relation'

	def execute(self, do_exec = True):
		# check permissions
		self.__check_perm()
		# create reference groups
		self.__analyze()
		# set default values
		self._set_default()

		if not do_exec:
			from error.do_not_exec import *
			raise do_not_exec()

		# execute pre-action function
		self._tbl.pre(self.__act_str)
		# execute SQL query
		self.__doit()
		# execute post-action function
		self._tbl.post(self.__act_str)

	def __check_perm(self):
		if not self._tbl.perm(self.__act_str):
			# TODO: make this a perm_denied exception
			raise error(err_error, errmsg.permission_denied)

	def __analyze(self):
		# add primary key relation
		# NB: This has to be done _after_ the other reference groups are built
		# for the reason described in the 'pk_submit_relation' class.
		# Fortunately this is done in the entity constructor so we don't stand
		# a chance of violating this condition here.
		self._tbl.add_rel(self.__get_pk_rel())

		missing_lock = False

		for ref_grp in self.__ref_group_vec:
			if ref_grp.generate_keylist(self.__act_str, self.__session,
					self._tbl):
				# If we need the primary key, we have to prompt for PKs only.
				if self.__fill_table and
						ref_grp.has_key(self._tbl.get_pk_vec()[0]):
					from error.missing_pk_lock import *
					raise missing_pk_lock()

				missing_lock = True

		# Fill the table with existing values. For some actions, such as 'list'
		# or 'submit' this would not make any sense.
		if self.__fill_table:
			self._tbl.fill_pk()

		if missing_lock:
			from error.missing_lock import *
			raise missing_lock()

	def __get_pk_rel(self):
		pk_vec = self._tbl.get_pk_vec()
		table = self._tbl.get_name()
		cond, outer_join = self._get_pk_cond_join(table, pk_vec[0])

		__import__(self._relation_class)

		return eval(self._relation_class + "(" + \
			"table = table, " + \
			"keys = dict(zip(pk_vec, pk_vec)), " + \
			"cond = cond is None and {} or { self.__act_str: cond }, " + \
			"outer_join = outer_join)")

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

		import lib.db_iface
		rset = db_iface.query(sql_query)

		if self.__save_rset:
			self._tbl.set_rset(rset)
