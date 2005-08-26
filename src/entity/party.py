
#  entity/party.py
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
		from users import rank_check

		ent_table.__init__(self, attributes = [
			('name', string(label.party, perm.submit, '', 10)),
			('status', choice(label.party_status, self.opt_status, perm.edit, 0)),
			('date', date(label.date, perm.all)),
			('organizer', string(label.organizer, perm.all, '', 10)),
			('location', string(label.location, perm.all, '', 128)),
			('entry_fee_advance', string(label.entry_fee_advance, perm.all, '', 16)),
			('entry_fee', string(label.entry_fee, perm.all, '', 16))
			],
			primary_keys = [ 'name' ],
			relations = [
				relation(
			table =	'users',
			keys = {	'organizer':	'username' },
			cond = { 'all':	"users.rank > 1" }) ],
			item_txt = {
				'edit': {
					'en': 'Party Settings',
					'de': 'Party Einstellungen' },
				'submit': {
					'en': 'Add Party',
					'de': 'Party hinzuf"ugen' },
				'view': {
					'en': 'View Parties',
					'de': 'Partys ansehen' },
				'delete': {
					'en': 'Delete Party',
					'de': 'Party l"oschen' } },
			perm = {
				'all':	rank_check(self, 2),
				'view':	True } )
