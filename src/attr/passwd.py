#
#  attr/passwd.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from string import *

class passwd(string):
	def __init__(self, label, perm = [], default = None, length = 128,
			chk_func_vec = []):
		string.__init__(self, label, perm, default, length, chk_func_vec)

	def accept(self, attr_act):
		attr_act.visit_passwd(self)
	
	def check(self, plain_pwd):
		from crypt import crypt

		return self._val == crypt(plain_pwd, self._val)
