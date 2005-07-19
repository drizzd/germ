#
#  party.py
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
	opt_status = [
		{ 'en': 'Announced', 'de': 'Angek"undigt' },
		{ 'en': 'Registration phase', 'de': 'Anmeldephase' },
		{ 'en': 'Party is on', 'de': 'Party l"auft gerade' },
		{ 'en': 'Party has ended', 'de': 'Party ist vor"uber' } ]

	def __init__(self):
		ent_table.__init__(self, name = __name__, attributes = [
			init('name', string(label.party, perm.submit, None, 10)),
			init('status', choice(label.party_status, perm.edit, 0, opt_status)),
			init('date', date(label.date, perm.all)),
			init('location', string(label.location, perm.all, None, 128)),
			init('entry_fee_advance', string(label.entry_fee_advance, perm.all, None, 16)),
			init('entry_fee', string(label.entry_fee, perm.all, None, 16))
			],
			primary_keys = [ 'name' ])
