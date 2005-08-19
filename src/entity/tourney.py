#
#  tourney.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from erm.ent_table import *

import txt.label
from erm.relation import *
from attr.attribute import perm
from attr.string import *

class tourney(ent_table):
	def __init__(self):
		opt_mode = [
			{ 'en': 'single elimination' },
			{ 'en': 'double elimination' },
			{ 'en': 'manual', 'de': 'manuell' } ]

		opt_phase = [
			# 1
			{ 'en': 'announced' ,
			  'de': 'angek"undigt' },
			# 2
			{ 'en': 'in preparation',
			  'de': 'in Vorbereitung' },
			# 3
			{ 'en': 'started',
			  'de': 'gestartet' },
			# 4
			{ 'en': 'finished',
			  'de': 'beendet' } ]

		ent_table.__init__(self, attributes = [
			('party', string(label.party, perm.submit, None, 10)),
			('name', string(label.tourney, perm.submit, None, 32)),
			('organizer', string(label.organizer, perm.all, None, 10)),
			('mode', choice(label.tourney_mode, perm.all, 0, opt_mode))
			('phase', choice(label.tourney_phase, perm.all, 0, opt_phase)),
			('teamsize', int(label.teamsize, perm.all, None, 2))
			],
			primary_keys = [ 'party', 'name' ],
			relations = [
				relation(
			table =	'users',
			keys =	{ 'organizer':		'username' }),
				relation(
			table =	'party',
			keys =	{ 'party':		'name' },
			# party must be on
			cond =	{ 'submit':	"party.status = 2" })
				])
