#
#  attribute.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from lib.error import *
import text.errmsg

class perm:
	all = [ 'view', 'edit', 'submit' ]
	view = [ 'view' ]
	edit = [ 'view', 'edit' ]
	submit = [ 'view', 'submit' ]
	none = []

class attribute:
	def __init__(self, label, perm, default):
		self.__label = label
		self.__perm = perm
		self.__def = default
		self._val = None

		self.__locked = False
		self.isset = False

	def lock(self):
		if not self.is_set():
			raise error(err_fail, errmsg.tried_locking_unset_attr)
		self.__locked = True

	def is_locked(self):
		return self.__locked

	def set(self, val):
		self.isset = self.do_set(val)
	
	def do_set(self, val)
		raise error(err_fail, errmsg.abstract_func)

	def is_set(self):
		return self.isset

	def default(self):
		return self.__default

	def sql_type(self):
		raise error(err_fail, errmsg.abstract_func)

	def sql_str(self):
		raise error(err_fail, errmsg.abstract_func)

	def perm(self, action):
		return action in __perm

	def get(self)
		return self._val

	def accept(self, attr_act):
		raise error(err_fail, errmsg.abstract_func)
