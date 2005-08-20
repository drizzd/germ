#
#  users.py
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

	def __init__(self):
		from lib import chk
		from lib import misc
		import cf

		ent_table.__init__(self, attributes = [
			('username', string(label.username, perm.submit, None, 10,
				[chk.identifier])),
			(cf.pwd_str, passwd(label.passwd, [ 'submit' ], None, 30)),
			('rank', choice(label.rank, self.opt_rank, perm.view, 0)),
			('privacy', choice(label.privacy, self.opt_privacy, perm.all, 1)),
			('surname', string(label.surname, perm.all, None, 64)),
			('forename', string(label.forename, perm.all, None, 64)),
			('residence', string(label.residence, perm.all, None, 128)),
			('email', string(label.email, perm.all, None, 128)),
			('icquin', string(label.icquin, perm.all, None, 16)),
			('homepage', string(label.homepage, perm.all, None, 128)),
			('genre', choice(label.genre, self.opt_genre, perm.all, 0)),
			('last_activity', date(label.last_activity, perm.view,
				misc.today))
			],
			primary_keys = [ 'username' ],
			condition = { 'edit': "users.username = '$userid'" })
