#
#  entity/tourney.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from germ.erm.ent_table import *
from germ.erm.relation import *

from germ.txt import label
from germ.attr.attribute import perm
from germ.attr.string import *
from germ.attr.choice import *
from germ.attr.int import *

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

		from users import rank_check

		ent_table.__init__(self, attributes = [
			('name', string(label.tourney, perm.all, None, 32)),
			('party', string(label.party, perm.all, '', 20)),
			('organizer', string(label.organizer, perm.all, '', 10)),
			('mode', choice(label.tourney_mode, opt_mode, perm.all, 0)),
			('phase', choice(label.tourney_phase, opt_phase, perm.edit, 0)),
			('teamsize', int(label.teamsize, perm.all, 1, 2)) ],
			primary_keys = [ 'party', 'name' ],
			relations = [
				relation(
			table =	'users',
			keys =	{ 'organizer':		'username' },
			cond = {	'all':	"users.rank > 1" } ),
				relation(
			table =	'party',
			keys =	{ 'party':	'name' },
			# party must be on
			cond =	{ 'submit':	"party.status = 1 OR party.status = 2" })
				],
			item_txt = {
				'edit': {
					'en': 'Tourney Settings',
					'de': 'Turniereinstellungen' },
				'submit': {
					'en': 'New Tourney',
					'de': 'Turnier hinzuf"ugen' },
				'view': {
					'en': 'Tourneys',
					'de': 'Turniere' },
				'delete': {
					'en': 'Delete Tourney',
					'de': 'Turnier l"oschen' } },
			perm = {
				'all':	rank_check(self, 2),
				'view':	True,
				'list': True } )
