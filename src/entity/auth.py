#
#  auth.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from erm.ent_virtual import *
from attr.string import *
from attr.plain_pwd import *
from txt import label
import cf

class auth(ent_virtual):
	def __init__(self):
		ent_virtual.__init__(self, attributes = [
			('username', string(label.username, [ 'submit' ], None, 10)),
			(cf.pwd_str, plain_pwd(label.passwd, [ 'submit' ], None, 30))
			],
			primary_keys = [ 'username' ])

		self.__user_table = 'users'

	def execute(self, do_exec = True):
		if not do_exec:
			from error.do_not_exec import do_not_exec
			raise do_not_exec()

		for attr in self._attr_map.itervalues():
			if not attr.is_set():
				from error.missing_parm import *
				raise missing_parm()

		from lib.db_iface import db_iface

		rset = db_iface.query("SELECT %s FROM %s WHERE %s" % \
			(cf.pwd_str, self.__user_table, self.get_attr_sql_pk()))

		if len(rset) > 1:
			# TODO: Make this an invalid_key exception. This could very well
			# occur by a user 'mistake'. On the other hand, can it still occur
			# if ref_group.generate_keylist did not complain?
			from error import *
			raise error(err_fail, "Ambiguous primary key: result has " + \
					"multiple records", "number of records: %s" % \
					len(rset))

		if len(rset) == 0:
			invalid_auth = True
		else:
			passwd = rset[0][0]

			invalid_auth = not self._attr_map[cf.pwd_str].check(passwd)

		if invalid_auth:
			from error.invalid_parm import *
			raise invalid_parm('Wrong username/password')

		self._session['userid'] = self._attr_map['username'].get()
