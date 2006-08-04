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
from germ.attr.int import int
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
			('round', int(label.round, perm.edit)),
			('stage', int(label.stage, perm.edit)),
			('bracket', choice(label.bracket, opt_bracket, perm.edit)),
			('id', int(label.id, perm.edit)),
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
					"(t1.bracket = 2 AND (2*t1.round + t1.stage) = " \
					"(SELECT MAX(2*t2.round + t2.stage) " \
					"FROM double_elimination AS t2 " \
					"WHERE t1.bracket = t2.bracket)) OR " \
					"(t1.bracket = 1 AND (2*t1.round + t1.stage) = " \
					"(SELECT MAX(2*t2.round + t2.stage) " \
					"FROM double_elimination AS t2 " \
					"WHERE 1))" } ),
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
				if status > 1:
					round[bracket-1][stage] = rnd
				else:
					round[bracket-1][stage] = -rnd

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

				rset = sql_query("SELECT CASE status - 2 " \
						"WHEN 0 THEN team1 " \
						"WHEN 1 THEN team2 " \
						"ELSE NULL END " \
						"FROM %s WHERE party = '%s' AND tourney = '%s' AND " \
						"round = %s AND bracket = 1 " \
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
				rset = sql_query("SELECT CASE status-2 XOR bracket-1 " \
						"WHEN 0 THEN team2 " \
						"WHEN 1 THEN team1 " \
						"ELSE NULL END " \
						"FROM %s WHERE " \
						"party = '%s' AND tourney = '%s' AND " \
						"round = %s " \
						"ORDER BY id - (bracket - 1) * (2 * (id %% 2) - 1), " \
						"bracket" % (self._name, party, tourney, rnd),
						self._session, self._globals)

				final = False
				self._create_round(rset, party, tourney, rnd, 2, 1)
			elif round[1][1] > 0 and abs(round[1][0]) == round[1][1]:
				# Create new loser round.

				rnd = round[1][1]

				rset = sql_query("SELECT CASE status - 2 " \
						"WHEN 0 THEN team1 " \
						"WHEN 1 THEN team2 " \
						"ELSE NULL END " \
						"FROM %s WHERE " \
						"party = '%s' AND tourney = '%s' AND " \
						"round = %s AND bracket = 2 AND stage = 1 " \
						"ORDER BY id" % \
						(self._name, party, tourney, rnd),
						self._session, self._globals)

				if len(rset) > 1:
					final = False
					self._create_round(rset, party, tourney, rnd, 2)
			elif round[1][0] == 0 and round[0][0] != -1:
				# Create first loser round.

				rnd = 1

				rset = sql_query("SELECT CASE status - 2 " \
						"WHEN 0 THEN team2 " \
						"WHEN 1 THEN team1 " \
						"ELSE NULL END " \
						"FROM %s WHERE " \
						"party = '%s' AND tourney = '%s' AND " \
						"round = %s AND bracket = 1 " \
						"ORDER BY id" % \
						(self._name, party, tourney, rnd),
						self._session, self._globals)

				final = False
				self._create_round(rset, party, tourney, rnd, 2)
			else:
				final = False

			if final:
				# Create final round.

				rset = sql_query("SELECT CASE status - 2 " \
						"WHEN 0 THEN team1 " \
						"WHEN 1 THEN team2 " \
						"ELSE NULL END " \
						"FROM %s WHERE " \
						"party = '%s' AND tourney = '%s' AND " \
						"round = %s AND " \
						"(bracket = 1 OR (bracket = 2 AND stage = 1)) " \
						"ORDER BY bracket" % \
						(self._name, party, tourney, rnd),
						self._session, self._globals)

				self._create_round(rset, party, tourney, rnd, 2, 0)

	def start(cls, party, tourney, teams, session, glob):
		import random

		random.shuffle(teams)

		nr_teams = len(teams)

		py_int = type(0)

		from math import ceil, log, floor

		byes = 2**py_int(ceil(log(nr_teams,2))) - nr_teams

		spacing = py_int(floor((byes + nr_teams)/byes))

		# TODO: Distribute byes more evenly.
		for i in xrange(byes):
			teams.insert(spacing*i | 1, 'bye')

		for i in xrange(len(teams)/2):
			t1 = teams[2*i]
			t2 = teams[2*i+1]

			if t1 == 'bye':
				# team 2 wins
				status = 3
			elif t2 == 'bye':
				# team 1 wins
				status = 2
			else:
				# pending
				status = 1

			query_str = "INSERT INTO %s SET tourney = '%s', party = '%s', " \
					"round = 1, stage = 0, bracket = 1, id = %s, " \
					"team1 = '%s', team2 = '%s', status = '%s' " \
					% (cls.__name__, tourney, party, i, t1, t2, status)

			from germ.erm.helper import sql_query

			sql_query(query_str, session, glob)

	start = classmethod(start)

	def _create_round(self, rset, party, tourney, rnd, bracket = 1, stage = 0):
		py_int = type(0)

		rnd = rnd + py_int(not stage)

		recs = []
		for i in xrange(len(rset)/2):
			team1 = rset[2*i][0]
			team2 = rset[2*i+1][0]

			if team2 == 'bye':
				status = 2
			elif team1 == 'bye':
				status = 3
			else:
				status = 1
			
			recs.append('(' + ', '.join(["'" + str(i) + "'" for i in [party,
				tourney, rnd, stage, bracket, i, team1, team2, status]]) + \
				')')

		from germ.erm.helper import sql_query

		return sql_query("INSERT INTO %s " \
				"(party, tourney, round, stage, bracket, id, team1, team2, " \
				"status) VALUES %s" %
				(self._name, ', '.join(recs)), self._session, self._globals)
