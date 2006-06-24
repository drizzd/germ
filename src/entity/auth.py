#
#  entity/auth.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from germ.erm.ent_virtual import *

from germ.attr.string import *
from germ.attr.plain_pwd import *
from germ.txt import label
import cf

class auth(ent_virtual):
	__user_table = 'users'

	def __init__(self):
		ent_virtual.__init__(self, attributes = [
			('username', string(label.username, [ 'submit', 'edit' ], '', 10)),
			(cf.pwd_str + 'old', plain_pwd(label.passwd_old, [ 'edit' ], '', 30)),
			(cf.pwd_str, plain_pwd(label.passwd, [ 'submit', 'edit' ], '', 30)) ],
				primary_keys = [ ],
				action_txt = {
					'edit': {
						'en':	'change password',
						'de':	'Passwort "andern' },
					'submit': {
						'en':	'login',
						'de':	'einloggen' },
					'delete': {
						'en':	'log out',
						'de':	'ausloggen' } },
				action_report = {
					'edit': {
						'en':	'The password has been changed',
						'de':	'Das Passwort wurde ge"andert' },
					'submit': {
						'en':	'You have logged in',
						'de':	'Sie wurden eingeloggt' },
					'delete': {
						'en':	'You have logged out',
						'de':	'Sie wurden ausgeloggt' } })

	def require_parms(self, act_str):
		for attr in self._attr_map.itervalues():
			if attr.perm(act_str) and not attr.is_set():
				from germ.error.missing_parm import missing_parm
				raise missing_parm()

	def check_exec(self, do_exec):
		if not do_exec:
			from germ.error.do_not_exec import do_not_exec
			raise do_not_exec()

	def check_pwd(self, aid):
		from germ.erm.helper import sql_query

		rset = sql_query("SELECT %s FROM %s WHERE username = '%s'" % \
			(cf.pwd_str, self.__user_table,
			self._attr_map['username'].sql_str()), self._session,
			self._globals)

		if len(rset) > 1:
			# TODO: Make this an invalid_key exception. This could very well
			# occur by a user 'mistake'. On the other hand, can it still occur
			# if ref_group.generate_keylist did not complain?
			from germ.error.error import error
			raise error(error.fail, "Ambiguous primary key: result has " + \
					"multiple records", "number of records: %s" % \
					len(rset))

		if len(rset) == 0:
			invalid_auth = True
		else:
			passwd = rset[0][0]

			invalid_auth = not self._attr_map[aid].check(passwd)

		if invalid_auth:
			from germ.error.invalid_parm import invalid_parm
			raise invalid_parm('Wrong username/password')

	def edit(self, act_str, do_exec = True):
		self.check_exec(do_exec)

		self.require_parms(act_str)

		self.check_pwd(cf.pwd_str + 'old')

		from germ.attr.passwd import passwd
		attr = passwd(label.passwd, [ 'submit' ], '', 30)
		attr.set(self._attr_map[cf.pwd_str].get())

		from germ.erm.helper import sql_query

		rset = sql_query("UPDATE %s SET %s = '%s' WHERE username = '%s'" % \
			(self.__user_table, cf.pwd_str, attr.sql_str(),
				self._attr_map['username'].sql_str()), self._session,
			self._globals)

	def submit(self, act_str, do_exec = True):
		if self._session.has_key('userid'):
			from germ.error.no_valid_keys import no_valid_keys
			raise no_valid_keys()

		self.check_exec(do_exec)

		self.require_parms(act_str)

		self.check_pwd(cf.pwd_str)

		self._session['userid'] = self._attr_map['username'].get()

	def delete(self, act_str, do_exec = True):
		if not self._session.has_key('userid'):
			from germ.error.no_valid_keys import no_valid_keys
			raise no_valid_keys()

		self.check_exec(do_exec)

		del self._session['userid']
