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
			{ 'en': 'manual', 'de': 'manuell' },
			{ 'en': 'single elimination' },
			{ 'en': 'double elimination' } ]

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
			('mode', choice(label.tourney_mode, opt_mode, perm.all)),
			('phase', choice(label.tourney_phase, opt_phase, perm.edit)),
			('teamsize', int(label.teamsize, perm.all, 1, 2)) ],
			primary_keys = [ 'party', 'name' ],
			relations = [
				relation(
			table = 'tourney',
			alias = 'tn',
			keys = {	'party':	'party',
						'name':		'name' },
			cond =	{
				'delete':	"tn.phase IN (0)",
				'edit':		"tn.phase IN (0, 1)" },
			outer_join = "LEFT" ),
				relation(
			table =	'users',
			alias = 'orga',
			keys =	{ 'organizer':		'username' },
			cond = {	'all':	"orga.rank > 0" } ),
				relation(
			table =	'party',
			keys =	{ 'party':	'name' },
			# party must be on
			cond =	{
				'submit':	"party.status IN (1, 2)",
				'edit':		"party.status IN (1, 2)" } )
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
				'list': {
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
			self._attr_map['phase'].set_mask([0])
		elif act_str == 'edit':
			phase = self.get_cur_attr('phase')

			mask = []

			if phase == 0:
				mask = [phase, phase + 1]
			elif phase == 1:
				from team_members import team_members

				party = self.get_attr_nocheck('party').get()
				tourney = self.get_attr_nocheck('name').get()
				size = self.get_attr_nocheck('teamsize').get()

				self.__teams = team_members.get_teams(party, tourney, size,
						self._session, self._globals)

				if len(self.__teams) >= 2:
					mask = [phase, phase + 1]
				else:
					mask = [phase]
			else:
				from germ.error.error import error
				raise error(error.error, 'Attempt to edit tourney in ' \
						'phase %i' % phase)

			attr = self.get_attr_nocheck('phase')
			attr.set_mask(mask)

			self.__prev_phase = phase
			self.__next_phase = attr.get()

	def post(self, act_str):
		if act_str == 'edit':
			if self.__prev_phase == 1 and self.__next_phase == 2:
				attr = self.get_attr_nocheck('mode')
				mode = attr.get()

				if mode == 0:
					# TODO: Create ranking table if necessary.
					pass
				elif mode == 1:
					from germ.error.error import error
					raise error(error.error, 'Not yet implemented: %s' %
							str(attr))
				elif mode == 2:
					# double elimination

					party = self.get_attr_nocheck('party').get()
					tourney = self.get_attr_nocheck('name').get()

					from double_elimination import double_elimination

					double_elimination.start(party, tourney, self.__teams,
							self._session, self._globals)
				else:
					from germ.error.error import error
					raise error(error.error, 'Unknown mode %i' % mode)
