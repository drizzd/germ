#
#  table_action.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from error import *
import text.errmsg

class table_action:
	def __init__(self, act_str, table):
		self.__act_str = act_str
		self.__tbl = table

	def execute(self):
		# check permissions
		self.__check_perm()
		# create reference groups
		self.__analyze()
		# execute pre-action function
		self.__tbl.pre(self.__act_str)
		# execute SQL query
		self.__doit()
		# execute post-action function
		self.__tbl.post(self.__act_str)

	def __check_perm(self):
		if not self.__tbl.perm(self.__act_str):
			raise error(err_error, errmsg.permission_denied)

	def __analyze(self):
		# add primary key relation
		self.add_pk_rel()
		self.__tbl.generate_keylists(self.__act_str)
		self.check_pk_locks(self.__tbl)
		
	def add_pk_rel(self):
		self.__tbl.add_rel(self.__get_pk_rel())

	def __get_pk_rel(self):
		from relation import *

		pk_vec = self.__tbl.get_pk_vec()
		table = self.__tbl.get_name()
		cond, outer_join = self.get_pk_cond_join(table, pk_vec[0])

		return relation(
			table = table,
			keys = dict(zip(pk_vec, pk_vec)),
			cond = { self.__act_str: cond },
			outer_join = outer_join)
		
	def check_pk_locks(self, tbl):
		raise error(err_error, errmsg.abstract_func)

	def get_pk_cond_join(self, table, pk0):
		raise error(err_error, errmsg.abstract_func)

	def __doit(self):
		pass
