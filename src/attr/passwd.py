#
#  passwd.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from string import *

class passwd(string):
	def __init__(self, label, perm = {}, default = '', length = 128,
			chk_func_vec = []):
		string.__init__(self, label, perm, default, length, chk_func_vec)

	def accept(self, attr_act):
		attr_act.visit_passwd(self)

	def sql_str(self):
		import random
		string = __import__('string')
		salt = ''
		for i in range(2):
			salt += random.choice('./' + string.letters + string.digits)

		from crypt import crypt

		return crypt(self._val, salt)
