
#  party.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from erm.ent_table import *
from erm.relation import *

from txt import label
from attr.attribute import perm
from attr.string import *
from attr.date import *
from attr.choice import *

class party(ent_table):
	opt_status = [
		{ 'en': 'Announced', 'de': 'Angek"undigt' },
		{ 'en': 'Registration phase', 'de': 'Anmeldephase' },
		{ 'en': 'Party is on', 'de': 'Party l"auft gerade' },
		{ 'en': 'Party has ended', 'de': 'Party ist vor"uber' } ]

	def __init__(self):
		from lib.misc import rank_check

		ent_table.__init__(self, attributes = [
			('name', string(label.party, perm.submit, None, 10)),
			('status', choice(label.party_status, self.opt_status, perm.edit, 0)),
			('date', date(label.date, perm.all)),
			('organizer', string(label.organizer, perm.all, None, 10)),
			('location', string(label.location, perm.all, None, 128)),
			('entry_fee_advance', string(label.entry_fee_advance, perm.all, None, 16)),
			('entry_fee', string(label.entry_fee, perm.all, None, 16))
			],
			primary_keys = [ 'name' ],
			relations = [
				relation(
			table =	'users',
			keys = {	'organizer':	'username' },
			cond = "users.rank > 1" ) ],
			item_txt = {
				'edit': {
					'en': 'Party Settings',
					'de': 'Party Einstellungen' },
				'submit': {
					'en': 'New Party',
					'de': 'Party erstellen' },
				'delete': {
					'en': 'Delete Party',
					'de': 'Party l"oschen' } },
			perm = rank_check(self, 2) )
