#
#  users.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from erm.ent_table import *

import text.label
from erm.relation import *
from attr.attribute import perm
from attr.string import *

class users(ent_table):
	opt_rank = [
		{ 'en': 'Gamer', 'de': 'Spieler' },
		{ 'en': 'Assistant', 'de': 'Hilfsorga' },
		{ 'en': 'Staff', 'de': 'Orga' },
		{ 'en': 'Admin', 'de': 'Admin' } ]

	opt_genre = [
		{ 'en': 'indecisive', 'de': 'unentschlossen' },
		{ 'en': 'Action (CS, UT, Q3, ...)' },
		{ 'en': 'Strategy (C&C, Dune, SC, ...)' },
		{ 'en': 'Sport (NHL, FIFA, NFS, ...)' },
		{ 'en': 'Simulation (Commanche 4, ...)' },
		{ 'en': 'Adventure (Auryns Quest, Diablo, ...)' } ]
	
	opt_privacy = [
		{ 'en': 'show all', 'de': 'Alles anzeigen' },
		{ 'en': 'hide name and address', 'de': 'Name und Adresse geheimhalten' }
		{ 'en': 'hide all but nickname', 'de': 'Nur Nickname anzeigen' }

	def __init__(self):
		ent_table.__init__(self, name = __name__, attributes = [
			('username', string(label.username, perm.submit, None, 10)),
			('rank', choice(label.rank, perm.view, 0, opt_rank)),
			('genre', choice(label.genre, perm.all, 0, opt_genre)),
			('privacy', string(label.privacy, perm.all, 1, opt_privacy)),
			('forename', string(label.forename, perm.all, None, 64)),
			('surname', string(label.surname, perm.all, None, 64)),
			('address', string(label.address, perm.all, None, 128)),
			('email', string(label.email, perm.all, None, 128)),
			('icquin', string(label.icquin, perm.all, None, 16)),
			('homepage', string(label.homepage, perm.all, None, 128)),
			('passwd', string(label.passwd, [ 'edit', 'submit' ], None, 30)),
			('last_activity', date(label.last_activity, perm.view, None))
			],
			primary_keys = [ 'username' ])
