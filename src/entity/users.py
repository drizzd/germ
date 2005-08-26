#
#  entity/users.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from erm.ent_table import *

from txt import label
from erm.relation import *
from attr.attribute import perm
from attr.string import *
from attr.passwd import *
from attr.choice import *
from attr.date import *

class users(ent_table):
	__last_rank = (None, None)

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
			{	'en': 'hide all but nickname',
				'de': 'Nur Nickname anzeigen' } ]

		from lib import chk
		from lib.misc import var_check
		import cf

		ent_table.__init__(self, attributes = [
			('username', string(label.username, perm.submit, None, 10,
				[chk.identifier])),
			(cf.pwd_str, passwd(label.passwd, [ 'submit' ], '', 30)),
			('rank', choice(label.rank, opt_rank, perm.view, 0)),
			('privacy', choice(label.privacy, opt_privacy, perm.all, 1)),
			('surname', string(label.surname, perm.all, '', 64)),
			('forename', string(label.forename, perm.all, '', 64)),
			('residence', string(label.residence, perm.all, '', 128)),
			('email', string(label.email, perm.all, '', 128)),
			('icquin', string(label.icquin, perm.all, '', 16)),
			('homepage', string(label.homepage, perm.all, '', 128)),
			('genre', choice(label.genre, opt_genre, perm.all, 0)),
			('last_activity', date(label.last_activity, perm.view))
			],
			primary_keys = [ 'username' ],
			condition = { 'edit':	"users.username = $userid OR " \
									"$users.rank > 1" },
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
			perm = {	'submit':	var_check(self, 'userid', None) },
			magic_var = { 'rank':	self.__rank })

	def __rank(self):
		userid = self._session.get('userid')

		if userid is None:
			return 'NULL'

		return str(self.get_rank(userid))

	def get_rank(cls, userid):
		if cls.__last_rank[0] == userid:
			return cls.__last_rank[1]

		from lib.db_iface import db_iface

		rset = db_iface.query("SELECT rank FROM users WHERE username = '%s'" \
				% userid)

		if len(rset) != 1:
			from error.error import error
			raise error(error.fail, "Invalid userid", 'userid: %s' % userid)

		rec = rset[0]
		rank = int(rec[0])

		cls.__last_rank = (userid, rank)

		return rank

	get_rank = classmethod(get_rank)

class rank_check:
	def __init__(self, entity, rank):
		self.__entity = entity
		self.__rank = rank

	def __call__(self):
		userid = self.__entity.get_var('userid')

		if userid is None:
			return False

		rank = users.get_rank(userid)
		return rank >= self.__rank
