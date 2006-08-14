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
	def __init__(self):
		self.__prev_attr = (None, None, None)

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
			(cf.pwd_str, passwd(label.passwd, [ 'submit' ], '', 64)),
			('rank', choice(label.rank, opt_rank, perm_rank)),
			('privacy', choice(label.privacy, opt_privacy, perm.all)),
			('surname', string(label.surname, perm_privacy1, '', 64)),
			('forename', string(label.forename, perm_privacy1, '', 64)),
			('residence', string(label.residence, perm_privacy1, '', 128)),
			('email', string(label.email, perm_privacy2, '', 128)),
			('icquin', string(label.icquin, perm_privacy2, '', 16)),
			('homepage', string(label.homepage, perm_privacy2, '', 128)),
			('genre', choice(label.genre, opt_genre, perm_privacy2)),
			('last_activity', date(label.last_activity, perm_staff))
			],
			primary_keys = [ 'username' ],
			relations = [
				relation(
			table = 'users',
			alias = 'u',
			keys = {	'username':	'username' },
			cond = {
				'edit':
					# user may only edit other users of lower rank, and he may
					# only change their rank to one lower than his own;
					# user may only lower own rank (or leave it)
					"u.username = $userid OR u.rank < $users.rank" },
			outer_join = "LEFT" )
				],
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
		if not self.has_rec():
			return True

		rank = self.get_cur_attr('rank')
		
		if self.superior(rank):
			return True

		username = self.get_cur_attr('username')

		userid = self._session.get('userid')

		if userid is not None and userid == username:
			return True

		userprivacy = self.get_cur_attr('privacy')

		return userprivacy < privacy
	
	def check_privacy2(self, attr):
		return self.check_privacy1(attr, privacy = 2)

	def check_rank(self, attr):
		userid = self._session.get('userid')

		if userid is None:
			return False

		if not self.has_rec():
			return True

		rank = self.get_rank(userid)

		username = self.get_cur_attr('username')
		userrank = self.get_cur_attr('rank')

		if not (username == userid or rank > userrank):
			return False

		mask = range(rank)

		if username == userid:
			mask.append(rank)

		self.get_attr_nocheck('rank').set_mask(mask)

		return True

	def superior(self, rank):
		userid = self._session.get('userid')

		if userid is None:
			return False

		userrank = self.get_rank(userid)

		return userrank > rank

	def check_staff(self, attr):
		userid = self._session.get('userid')

		return userid is not None and self.get_rank(userid) > 0

	def get_rank(self, userid):
		return self.get_user_attr(userid, 'rank')

	def get_user_attr(self, userid, attr):
		if self.__prev_attr[0] == userid and self.__prev_attr[1] == attr:
			return self.__prev_attr[2]

		rec = self.get_rec_explicit('users', "username = '%s'" % userid, attr)

		res = rec[0]

		self.__prev_attr = (userid, attr, res)

		return res

class rank_check:
	def __init__(self, entity, rank):
		self.__entity = entity
		self.__rank = rank

	def __call__(self, attr = None):
		userid = self.__entity.get_var('userid')

		if userid is None:
			return False

		rank = self.__entity.get_rec_explicit('users', "username = '%s'" % \
				userid, 'rank')
		return rank >= self.__rank
