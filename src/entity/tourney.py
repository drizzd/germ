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

		self.__prev_phase = None
		self.__next_phase = None
		self.__teams = None

		from users import rank_check

		ent_table.__init__(self, attributes = [
			('name', string(label.tourney, perm.all + ['delete'], None, 32)),
			('party', string(label.party, perm.all + ['delete'], '', 20)),
			('organizer', string(label.organizer, perm.all, '', 10)),
			('mode', choice(label.tourney_mode, opt_mode, perm.all, 0)),
			('phase', choice(label.tourney_phase, opt_phase, perm.edit, 0)),
			('teamsize', int(label.teamsize, perm.all, 1, 2)) ],
			primary_keys = [ 'party', 'name' ],
			relations = [
				relation(
			table = 'tourney',
			alias = 'tn',
			keys = {	'party':	'party',
						'name':		'name' },
			cond =	{
				'delete':	"tn.phase = 1",
				'edit':		"tn.phase = 1 OR tn.phase = 2" } ),
				relation(
			table =	'users',
			alias = 'orga',
			keys =	{ 'organizer':		'username' },
			cond = {	'all':	"orga.rank > 1" } ),
				relation(
			table =	'party',
			keys =	{ 'party':	'name' },
			# party must be on
			cond =	{
				'submit':	"party.status = 1 OR party.status = 2",
				'edit':		"party.status = 1 OR party.status = 2" })
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

	def pre(self, act_str):
		if act_str == 'submit':
			self._attr_map['phase'].set_mask([1])
		elif act_str == 'edit':
			i = self._attr_ids.index('phase')
			phase = self._rset[0][i]

			mask = []

			if phase == 1:
				mask = [phase, phase + 1]
			elif phase == 2:
				from team_members import team_members

				party = self._attr_map['party'].get()
				tourney = self._attr_map['name'].get()
				size = self._attr_map['teamsize'].get()

				self.__teams = team_members.get_teams(party, tourney, size,
						self._session, self._globals)

				if len(self.__teams) >= 2:
					mask = [phase, phase + 1]
				else:
					mask = [phase]
			else:
				from germ.error.error import error
				raise error(error.error, 'Attempt to edit tourney in ' \
						'phase %i.' % phase)

			attr = self._attr_map['phase']
			attr.set_mask(mask)
			if attr.get() not in mask:
				attr.set(phase)

			self.__prev_phase = phase
			self.__next_phase = attr.get()

	def post(self, act_str):
		if act_str == 'edit':
			if self.__prev_phase == 2 and self.__next_phase == 3:
				attr = self._attr_map['mode']
				mode = attr.get()

				if mode == 2:
					# double elimination

					party = self._attr_map['party'].get()
					tourney = self._attr_map['name'].get()

					from double_elimination import double_elimination

					double_elimination.start(party, tourney, self.__teams,
							self._session, self._globals)
				elif mode == 3:
					pass
				else:
					from germ.error.error import error
					raise error(error.error, 'Not yet implemented: %s' %
							str(attr))
