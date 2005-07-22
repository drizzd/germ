#
#  table_action.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from error import *
import text.errmsg

class table_action:
	def __init__(self, act_str, table, require_pk_locks):
		self.__act_str = act_str
		self._tbl = table
		self.__require_pk_locks = require_pk_locks

	def execute(self):
		# check permissions
		self.__check_perm()
		# create reference groups
		self.__analyze()
		# execute pre-action function
		self._tbl.pre(self.__act_str)
		# execute SQL query
		self.__doit()
		# execute post-action function
		self._tbl.post(self.__act_str)

	def __check_perm(self):
		if not self._tbl.perm(self.__act_str):
			raise error(err_error, errmsg.permission_denied)

	def __analyze(self):
		# add primary key relation
		self.__add_pk_rel()
		self._tbl.generate_keylists(self.__act_str)

		if self.__require_pk_locks:
			self._tbl.require_pk_locks()
		
	def __add_pk_rel(self):
		self._tbl.add_rel(self.__get_pk_rel())

	def __get_pk_rel(self):
		from relation import *

		pk_vec = self._tbl.get_pk_vec()
		table = self._tbl.get_name()
		cond, outer_join = self.get_pk_cond_join(table, pk_vec[0])

		return relation(
			table = table,
			keys = dict(zip(pk_vec, pk_vec)),
			cond = { self.__act_str: cond },
			outer_join = outer_join)
		
	def _get_sql_query(self, table, sql_str):
		raise error(err_error, errmsg.abstract_func)

	def _get_pk_cond_join(self, table, pk0):
		raise error(err_error, errmsg.abstract_func)

	def __doit(self):
		sql_query = self._get_sql_query()

		import lib.db_iface
		db_iface.query(sql_query)
