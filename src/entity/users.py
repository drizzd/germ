#
#  entity/users.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from germ.erm.ent_table import *
from germ.erm.relation import *

from germ.txt import label
from germ.attr.attribute import perm
from germ.attr.string import *
from germ.attr.passwd import *
from germ.attr.choice import *
from germ.attr.date import *

# TODO: rank should be editable, but only if user rank >= staff, and only if edited
# rank < user rank
class users(ent_table):
	__prev_attr = (None, None)

	def __init__(self):
		opt_rank = [
			{ 'en': 'Gamer', 'de': 'Spieler' },
			{ 'en': 'Assistant', 'de': 'Hilfsorga' },
			{ 'en': 'Staff', 'de': 'Orga' },
			{ 'en': 'Admin', 'de': 'Admin' } ]

		opt_genre = [
			{ 'en': '-' },
			{ 'en': 'Action (CS, UT, Q3, ...)' },
			{ 'en': 'Strategy (C&C, Dune, SC, ...)' },
			{ 'en': 'Sport (NHL, FIFA, NFS, ...)' },
			{ 'en': 'Simulation (Comanche 4, ...)' },
			{ 'en': 'Adventure (Auryns Quest, ...)' } ]

		opt_privacy = [
			{	'en': 'show all',
				'de': 'Alles anzeigen' },
			{	'en': 'hide name and residence',
				'de': 'Name und Wohnort geheimhalten' },
			{	'en': 'hide all but username',
				'de': 'Nur Benutzernamen anzeigen' } ]

		perm_privacy1 = {
			'view':		self.check_privacy1,
			'edit':		True,
			'submit':	True }

		perm_privacy2 = {
			'view':		self.check_privacy2,
			'edit':		True,
			'submit':	True }

		perm_staff = { 'view':	self.check_staff }

		perm_rank = {
			'view':		self.check_privacy2,
			'edit':		self.check_rank }

		from germ.lib import chk
		from germ.lib.misc import var_check
		import cf

		ent_table.__init__(self, attributes = [
			('username', string(label.username, perm.all, None, 10,
				[chk.identifier])),
			(cf.pwd_str, passwd(label.passwd, [ 'submit' ], '', 30)),
			('rank', choice(label.rank, opt_rank, perm_rank, 0)),
			('privacy', choice(label.privacy, opt_privacy, perm.all, 1)),
			('surname', string(label.surname, perm_privacy1, '', 64)),
			('forename', string(label.forename, perm_privacy1, '', 64)),
			('residence', string(label.residence, perm_privacy1, '', 128)),
			('email', string(label.email, perm_privacy2, '', 128)),
			('icquin', string(label.icquin, perm_privacy2, '', 16)),
			('homepage', string(label.homepage, perm_privacy2, '', 128)),
			('genre', choice(label.genre, opt_genre, perm_privacy2, 0)),
			('last_activity', date(label.last_activity, perm_staff))
			],
			primary_keys = [ 'username' ],
			condition = {
				'edit':
					# TODO: this does not work as it should
					# user may only edit other users of lower rank, and he may
					# only change their rank to one lower than his own;
					# user may only lower own rank (or leave it)
					"users.username = $userid OR " \
					"($users.rank > 1 AND users.rank < $users.rank)" },
			item_txt = {
				'edit': {
					'en': 'My Profile',
					'de': 'Mein Profil' },
				'submit': {
					'en': 'Register',
					'de': 'Registrierung' },
				'view': {
					'en': 'Users',
					'de': 'Benutzer' } },
			action_report = {
				'submit': {
					'en': 'Your registration has been submitted',
					'de': 'Sie wurden registriert' } },
			perm = {	'submit':	var_check(self, 'userid', None) },
			magic_var = { 'rank':	self.__rank })

	def __rank(self):
		userid = self._session.get('userid')

		if userid is None:
			return 'NULL'

		return self.get_rank(userid)

	def check_privacy1(self, attr, privacy = 1):
		if self.check_superior(attr):
			return True

		userattr = self._attr_map['username']

		if not userattr.is_set():
			return True

		username = userattr.sql_str()

		userid = self._session.get('userid')

		if userid is not None and userid == username:
			return True

		userprivacy = self.get_user_attr(username, 'privacy')

		return userprivacy < privacy
	
	def check_privacy2(self, attr):
		return self.check_privacy1(attr, privacy = 2)

	def check_rank(self, attr):
		userid = self._session.get('userid')

		if userid is None:
			return False

		rank = self.get_rank(userid)

		userattr = self._attr_map['username']

		if not userattr.is_set():
			return True

		username = userattr.sql_str()
		userrank = self.get_rank(username)

		if not rank > userrank:
			return False

		if attr.is_set() and attr.get() >= rank:
			attr.set(rank - 1)

		return True

	def check_superior(self, attr):
		userid = self._session.get('userid')

		if userid is None:
			return False

		rank = self.get_rank(userid)

		userattr = self._attr_map['username']
		
		if not userattr.is_set():
			return True

		username = userattr.sql_str()
		userrank = self.get_rank(username)

		return rank > userrank

	def check_staff(self, attr):
		userid = self._session.get('userid')

		return userid is not None and self.get_rank(userid) >= 2

	def get_rank(cls, userid):
		return cls.get_user_attr(userid, 'rank')

	get_rank = classmethod(get_rank)
	
	# TODO: move this to ent_table
	def get_user_attr(cls, userid, attr):
		if cls.__prev_attr[0] == userid and cls.__prev_attr[1] == attr:
			return cls.__prev_attr[2]

		from germ.lib.db_iface import db_iface

		rset = db_iface.query("SELECT %s FROM users WHERE username = '%s'" \
				% (attr, userid))

		if len(rset) != 1:
			from germ.error.error import error
			raise error(error.fail, "Invalid userid", 'userid: %s' % userid)

		rec = rset[0]
		res = rec[0]

		cls.__prev_attr = (userid, attr, res)

		return res

	get_user_attr = classmethod(get_user_attr)

class rank_check:
	def __init__(self, entity, rank):
		self.__entity = entity
		self.__rank = rank

	def __call__(self, attr = None):
		userid = self.__entity.get_var('userid')

		if userid is None:
			return False

		rank = users.get_rank(userid)
		return rank >= self.__rank
