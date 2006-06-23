#
#  attr/plain_pwd.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from string import *

class plain_pwd(string):
	def __init__(self, label, perm = [], default = None, length = 32,
			chk_func_vec = []):
		string.__init__(self, label, perm, default, length, chk_func_vec)

	def accept(self, attr_act):
		attr_act.visit_plain_pwd(self)

	def check(self, crypted_pwd):
		from crypt import crypt

		from germ.error.error import error
		error(error.debug, 'checking password %s (%s)' % (self._val, crypted_pwd))
		return crypted_pwd == crypt(self._val, crypted_pwd)
