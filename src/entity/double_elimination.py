#
#  entity/double_elimination.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from germ.erm.ent_table import ent_table
from germ.erm.relation import relation

from germ.txt import label
from germ.attr.attribute import perm
from germ.attr.string import string
from germ.attr.bool import bool
from germ.attr.int import int as attr_int
from germ.attr.choice import choice

class double_elimination(ent_table):
	def __init__(self):
		opt_bracket = [
			{ 'en': 'Winner' },
			{ 'en': 'Loser' } ]

		opt_status = [
			{ 'en': 'pending',
			  'de': 'l"auft' },
			{ 'en': 'Team 1 wins',
			  'de': 'Team 1 gewinnt' },
			{ 'en': 'Team 2 wins',
			  'de': 'Team 2 gewinnt' } ]

		from users import rank_check

		ent_table.__init__(self, attributes = [
			('party', string(label.party, perm.all, '', 20)),
			('tourney', string(label.tourney, perm.all, '', 32)),
			('round', attr_int(label.round, perm.edit)),
			('stage', attr_int(label.stage, perm.edit)),
			('bracket', choice(label.bracket, opt_bracket, perm.edit)),
			('id', attr_int(label.id, perm.edit)),
			('team1', string(label.team1, perm.view, '', 32)),
			('team2', string(label.team2, perm.view, '', 32)),
			('status', choice(label.status, opt_status, perm.edit))
			],
			primary_keys = [ 'party', 'tourney',
				'round', 'stage', 'bracket', 'id' ],
			relations = [
				relation(
			table = 'double_elimination',
			alias = 't1',
			keys = {	'party':	'party',
						'tourney':	'tourney',
						'round':	'round',
						'stage':	'stage',
						'bracket':	'bracket',
						'id':		'id' },
			# TODO: Is there a neater way to do this and can we get rid of the
			# nested SELECT?
			cond = {	'edit':
					"(t1.bracket = 1 AND (2*t1.round + t1.stage) = " \
					"(SELECT MAX(2*t2.round + t2.stage) " \
					"FROM double_elimination AS t2 " \
					"WHERE t1.party = t2.party AND t1.tourney = t2.tourney AND t1.bracket = t2.bracket)) OR " \
					"(t1.bracket = 0 AND (2*t1.round + t1.stage) = " \
					"(SELECT MAX(2*t2.round + t2.stage) " \
					"FROM double_elimination AS t2 " \
					"WHERE t1.party = t2.party AND t1.tourney = t2.tourney))" } ),
				relation(
			table =	'team',
			alias = 'tm1',
			keys = {	'party':	'party',
						'tourney':	'tourney',
						'team1':	'name' } ),
				relation(
			table =	'team',
			alias = 'tm2',
			keys = {	'party':	'party',
						'tourney':	'tourney',
						'team2':	'name' } ) ],
			perm = {
				'edit':	rank_check(self, 2),
				'view': True },
			item_txt = {
				'edit': {
					'en': 'Enter game results',
					'de': 'Spielergebnisse eintragen' },
				'submit': {
					'en': 'Add game',
					'de': 'Spiel hinzuf"ugen' },
				'list': {
					'en': 'Game results',
					'de': 'Spielergebnisse' } }
				)

	def post(self, act_str):
		if act_str == 'edit':
			party = self._attr_map['party'].get()
			tourney = self._attr_map['tourney'].get()

			query_str = "SELECT bracket, MAX(round), stage, MIN(status) " \
					"FROM %s " \
					"WHERE party = '%s' AND tourney = '%s' " \
					"GROUP BY bracket, stage" % \
					(self._name, party, tourney)
					
			from germ.erm.helper import sql_query

			rset = sql_query(query_str, self._session, self._globals)

			round = [ [0, 0], [0, 0] ]

			for bracket, rnd, stage, status in rset:
				if status > 0:
					round[bracket][stage] = rnd
				else:
					round[bracket][stage] = -rnd

			if abs(round[1][0]) > abs(round[0][0]):
				# Tourney is finished.
				sql_query("UPDATE tourney SET phase = 4 WHERE " \
						"party = '%s' AND name = '%s'" % \
						(party, tourney),
						self._session, self._globals)
				return

			final = False

			if round[0][0] > 0:
				# Create new winner round.

				rnd = round[0][0]

				rset = sql_query("SELECT CASE status - 1 " \
						"WHEN 1 THEN team1 " \
						"WHEN 2 THEN team2 " \
						"ELSE NULL END " \
						"FROM %s WHERE party = '%s' AND tourney = '%s' AND " \
						"round = %s AND bracket = 0 " \
						"ORDER BY id" % \
						(self._name, party, tourney, rnd),
						self._session, self._globals)

				final = len(rset) == 1

				if not final:
					self._create_round(rset, party, tourney, rnd)

			if round[1][0] > 0 and abs(round[1][1]) < round[1][0] and \
					(round[0][0] >= round[1][0] or -round[0][0] > round[1][0]):
				# Create new loser stage.

				rnd = round[1][0]

				# Align losers of winner bracket and winners of loser
				# bracket. Also swap neighbouring loser positions to reduce
				# the chance of rematches.
				rset = sql_query("SELECT CASE (status - 1) XOR bracket " \
						"WHEN 0 THEN team2 " \
						"WHEN 1 THEN team1 " \
						"ELSE NULL END " \
						"FROM %s WHERE " \
						"party = '%s' AND tourney = '%s' AND " \
						"round = %s " \
						"ORDER BY id - bracket * (2 * (id %% 2) - 1), " \
						"bracket" % (self._name, party, tourney, rnd),
						self._session, self._globals)

				final = False
				self._create_round(rset, party, tourney, rnd, 2, 1)
			elif round[1][1] > 0 and abs(round[1][0]) == round[1][1]:
				# Create new loser round.

				rnd = round[1][1]

				rset = sql_query("SELECT CASE status " \
						"WHEN 1 THEN team1 " \
						"WHEN 2 THEN team2 " \
						"ELSE NULL END " \
						"FROM %s WHERE " \
						"party = '%s' AND tourney = '%s' AND " \
						"round = %s AND bracket = 1 AND stage = 1 " \
						"ORDER BY id" % \
						(self._name, party, tourney, rnd),
						self._session, self._globals)

				if len(rset) > 1:
					final = False
					self._create_round(rset, party, tourney, rnd, 2)
			elif round[1][0] == 0 and round[0][0] != -1:
				# Create first loser round.

				rnd = 1

				rset = sql_query("SELECT CASE status " \
						"WHEN 1 THEN team2 " \
						"WHEN 2 THEN team1 " \
						"ELSE NULL END " \
						"FROM %s WHERE " \
						"party = '%s' AND tourney = '%s' AND " \
						"round = %s AND bracket = 0 " \
						"ORDER BY id" % \
						(self._name, party, tourney, rnd),
						self._session, self._globals)

				final = False
				self._create_round(rset, party, tourney, rnd, 2)
			else:
				final = False

			if final:
				# Create final round.

				rset = sql_query("SELECT CASE status " \
						"WHEN 1 THEN team1 " \
						"WHEN 2 THEN team2 " \
						"ELSE NULL END " \
						"FROM %s WHERE " \
						"party = '%s' AND tourney = '%s' AND " \
						"round = %s AND " \
						"(bracket = 0 OR (bracket = 1 AND stage = 1)) " \
						"ORDER BY bracket" % \
						(self._name, party, tourney, rnd),
						self._session, self._globals)

				self._create_round(rset, party, tourney, rnd, 2, 0)

	def start(cls, party, tourney, teams, session, glob):
		import random

		random.shuffle(teams)

		nr_teams = len(teams)

		from math import ceil, log, floor

		byes = 2**int(ceil(log(nr_teams,2))) - nr_teams

		if byes > 0:
			spacing = (byes + nr_teams)/byes/2

		for i in xrange(byes):
			teams.insert(2*int(floor(spacing*i)) + 1, 'bye')

		rnd = 1
		bracket = 0
		stage = 0

		cls.insert_round(teams, party, tourney, rnd, bracket, stage, session,
				glob)

	start = classmethod(start)

	def _create_round(self, rset, party, tourney, rnd, bracket = 0, stage = 0):
		rnd = rnd + int(not stage)

		teams = []
		for i in rset:
			teams.append(i[0])

		self.insert_round(teams, party, tourney, rnd, bracket, stage,
				self._session, self._globals)

	def insert_round(cls, teams, party, tourney, rnd, bracket, stage,
			session, glob):
		recs = []
		for i in xrange(len(teams)/2):
			team1 = teams[2*i]
			team2 = teams[2*i+1]

			if team1 == 'bye':
				status = 2
			elif team2 == 'bye':
				status = 1
			else:
				status = 0
			
			recs.append('(' + ', '.join(["'" + str(i) + "'" for i in [party,
				tourney, rnd, stage, bracket, i, team1, team2, status]]) + \
				')')

		from germ.erm.helper import sql_query

		return sql_query("INSERT INTO %s " \
				"(party, tourney, round, stage, bracket, id, team1, team2, " \
				"status) VALUES %s" %
				(self._name, ', '.join(recs)), session, glob)

	insert_round = classmethod(insert_round)
