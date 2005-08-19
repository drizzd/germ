#
#  party.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from erm.ent_table import *

import txt.label
from erm.relation import *
from attr.attribute import perm
from attr.string import *
from attr.date import *

class users(ent_table):
	opt_status = [
		{ 'en': 'Announced', 'de': 'Angek"undigt' },
		{ 'en': 'Registration phase', 'de': 'Anmeldephase' },
		{ 'en': 'Party is on', 'de': 'Party l"auft gerade' },
		{ 'en': 'Party has ended', 'de': 'Party ist vor"uber' } ]

	def __init__(self):
		ent_table.__init__(self, attributes = [
			('name', string(label.party, perm.submit, None, 10)),
			('status', choice(label.party_status, perm.edit, 0, opt_status)),
			('date', date(label.date, perm.all)),
			('location', string(label.location, perm.all, None, 128)),
			('entry_fee_advance', string(label.entry_fee_advance, perm.all, None, 16)),
			('entry_fee', string(label.entry_fee, perm.all, None, 16))
			],
			primary_keys = [ 'name' ])
