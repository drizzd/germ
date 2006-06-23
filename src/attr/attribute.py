
#  attr/attribute.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from germ.txt import errmsg

class perm:
	all = [ 'view', 'edit', 'submit' ]
	view = [ 'view' ]
	edit = [ 'view', 'edit' ]
	submit = [ 'view', 'submit' ]
	none = []

class attribute:
	def __init__(self, label, perm, default, chk_func_vec):
		self.__label = label
		self.__perm = perm

		self.__default = default

		self._val = None
		self.__chk_func_vec = chk_func_vec

		self.__locked = False
		self.__to_lock = False
		self.__error_vec = []

	def copy_val(self):
		from copy import deepcopy

		self._val = deepcopy(self._val)

	def copy(self):
		from copy import copy

		dup = copy(self)
		dup.copy_val()

		return dup

	def label(self):
		from germ.lib import misc

		return misc.txt_lang(self.__label)

	def to_lock(self):
		if not self.is_set():
			from germ.error.error import error
			raise error(error.fail, errmsg.tried_locking_unset_attr)
		else:
			self.__to_lock = True

	def is_to_be_locked(self):
		return self.__to_lock

	def lock(self):
		if not self.is_set():
			from germ.error.error import error
			raise error(error.fail, errmsg.tried_locking_unset_attr)
		else:
			self.__locked = True

	def is_locked(self):
		return self.__locked

	def set_sql(self, val):
		self._val = val

	def unset(self):
		self._val = None

	def set(self, val):
		for chk_func in self.__chk_func_vec:
			res = chk_func(val)

			from germ.error.error import error
			if isinstance(res, error):
				self._error(res)

			if res is not None:
				val = res

		self._do_set(val)

	def _do_set(self, val):
		from germ.error.error import error
		raise error(error.fail, errmsg.abstract_func, 'class: %s' % self.__class__)

	def is_set(self):
		return self._val is not None

	def set_default(self):
		if self.__default is None:
			return

		from germ.lib.misc import call_if
		self.set(call_if(self.__default))

	def sql_type(self):
		from germ.error.error import error
		raise error(error.fail, errmsg.abstract_func)

	def sql_str(self):
		from germ.lib.db_iface import db_iface

		string = self._sql_str()

		if string is None:
			from germ.error.error import error
			raise error(error.error, 'Invalid SQL String', 'attr: %s' % \
					self.__class__.__name__)

		return db_iface.escape_string(string)

	def _sql_str(self):
		from germ.error.error import error
		raise error(error.fail, errmsg.abstract_func)

	def perm(self, action):
		return action in self.__perm

	def dyn_perm(self, action):
		from germ.lib.misc import always_false, always_true, call_if

		if isinstance(self.__perm, dict):
			# TODO: always return true self.__perm.has_key but PK not set
			return call_if(self.__perm.get(action, always_false), self)
		else:
			from germ.error.error import error
			error(error.debug, 'dyn_perm: not a dict')

			return self.perm(action)

	def get(self):
		return self._val

	def accept(self, attr_act):
		from germ.error.error import error
		raise error(error.fail, errmsg.abstract_func)

	def invalid_key(self):
		from germ.error.invalid_key import invalid_key
		self.__error_vec.append(invalid_key())

	def _error(self, e):
		self.__error_vec.append(e)

		from germ.error.invalid_parm import invalid_parm
		raise invalid_parm()

	def get_error(self):
		return self.__error_vec

	def _format_error(self):
		from germ.error.error import error
		raise error(error.fail, "Parameter has invalid format", "type: %s" % \
			self.__class__.__name__)
