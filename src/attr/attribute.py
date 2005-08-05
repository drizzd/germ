#
#  attribute.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from error.error import *
from text import errmsg

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
		self.__default = default
		self._val = None

		self.__locked = False
		self.__to_lock = False
		self.__is_set = False
		self.__error_vec = []

	def label(self):
		return self.__label

	def to_lock(self):
		if not self.__is_set:
			# Do not report this to user
			error(err_warn, errmsg.tried_locking_unset_attr)
		else:
			self.__to_lock = True

	def is_to_be_locked(self):
		return self.__to_lock

	def lock(self):
		if not self.__is_set:
			# Do not report this to user
			error(err_warn, errmsg.tried_locking_unset_attr)
		else:
			self.__locked = True

	def is_locked(self):
		return self.__locked

	def set_sql(self, val):
		self._val = val

	def set(self, val):
		raise error(err_fail, errmsg.abstract_func)

	def is_set(self):
		return self._val is not None

	def default(self):
		return self.__default

	def set_default(self):
		self.set(self.__default)

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

	def invalid_key(self):
		from error.invalid_key import *
		self.__error_vec.append(invalid_key())

	def _error(self, e):
		self.__error_vec.append(e)

		from error.invalid_parm import *
		raise invalid_parm()

	def _format_error(self):
		from error.error import *
		raise error(err_fail, "Parameter has invalid format", "type: %s" % \
			self.__class__.__name__)
