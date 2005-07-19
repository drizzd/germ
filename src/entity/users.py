#
#  users.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from erm.ent_table import *
import text.label
from attribute.string import *
from erm.relation import *
import erm.perm

from erm.attribute import *

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
			init('username', string(label.username, perm.submit, None, 10)),
			init('rank', choice(label.rank, perm.view, 0, opt_rank)),
			init('genre', choice(label.genre, perm.all, 0, opt_genre)),
			init('privacy', string(label.privacy, perm.all, 1, opt_privacy)),
			init('forename', string(label.forename, perm.all, None, 64)),
			init('surname', string(label.surname, perm.all, None, 64)),
			init('address', string(label.address, perm.all, None, 128)),
			init('email', string(label.email, perm.all, None, 128)),
			init('icquin', string(label.icquin, perm.all, None, 16)),
			init('homepage', string(label.homepage, perm.all, None, 128)),
			init('passwd', string(label.passwd, [ 'edit', 'submit' ], None, 30)),
			init('last_activity', date(label.last_activity, perm.view, None))
			],
			primary_keys = [ 'username' ])
