#
#  entity/team_members.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from germ.erm.ent_table import ent_table
from germ.erm.relation import relation

from germ.txt import label
from germ.attr.attribute import perm
from germ.attr.string import string
from germ.attr.bool import bool

class team_members(ent_table):
	def __init__(self):
		ent_table.__init__(self, attributes = [
			('party', string(label.party, perm.all + ['delete'], '', 20)),
			('username', string(label.username, perm.all + ['delete'], '', 10)),
			('tourney', string(label.tourney, perm.all + ['delete', 'list'], '', 32)),
			# Editing the team must not be allowed, because the 'active' status
			# would remain unchanged. The only legal way is to delete the entry
			# altogether and rejoin the other team.
			('team', string(label.team, perm.submit, '', 32)),
			('active', bool(label.active, perm.edit, 0))
			],
			primary_keys = [ 'party', 'username', 'tourney' ],
			relations = [
				relation(
			table =	'gamer',
			keys = {	'party':	'party',
						'username':	'username' },
						# Users can only subscribe themselves.
			cond = {	'submit':	"gamer.username = $userid",
						'delete':	"gamer.username = $userid OR " \
									"$users.rank > 0" } ),
				relation(
			table =	'team',
			keys = {	'party':	'party',
						'tourney':	'tourney',
						'team':		'name' },
						# Only the team leader can change member settings.
						#
						# NB: The 'team.name = team_members.team' condition can
						# not be handled as a join condition because 'team' is
						# not a primary key of 'team_members'.
			cond = {	'edit':		"team.name = team_members.team AND " \
									"team.leader = $userid" } ),
				relation(
			table =	'tourney',
			alias =	'tn',
			keys = {	'party':	'party',
						'tourney':	'name' },
						# Make sure tournament is in preparation phase.
			cond = {	'submit':	"tn.phase = 1",
						'edit':		"tn.phase = 1",
						'delete':	"tn.phase = 1" } ),
				relation(
			table =	'users',
			keys = {	'username':		'username' },
						# Make sure user has paid.
			cond = {	'submit':	"gamer.paid = TRUE OR users.rank > 0" } ),
				relation(
			table =	'team',
			alias =	'lt',
			keys = {	'party':	'party',
						'tourney':	'tourney',
						'username':	'leader' },
						# Make sure user is not a leader of another team
						# already.
			cond = {	'submit':	"lt.leader IS NULL OR team.name = lt.name" },
			outer_join =	"LEFT" )
				],
			item_txt = {
				'edit': {
					'en': 'Teammember Settings',
					'de': 'Teammitglieder Einstellungen' },
				'submit': {
					'en': 'Join Team',
					'de': 'Team beitreten' },
				'view': {
					'en': 'Teammembers',
					'de': 'Teammitglieder' },
				'list': {
					'en': 'Teammembers',
					'de': 'Teammitglieder' } } )

	def get_teams(cls, party, tourney, size, session, glob):
		import cf
		require_activation = cf.require_activation and size > 1

		query_str = "SELECT team FROM %s WHERE " \
				"party = '%s' AND tourney = '%s' %s " \
				"GROUP BY team %s" % \
				(cls.__name__, party, tourney,
					require_activation and "AND active = TRUE" or '',
					require_activation and "HAVING COUNT(1) >= %s" % size or '')

		from germ.erm.helper import sql_query

		rset = sql_query(query_str, session, glob)

		return [i[0] for i in rset]

	get_teams = classmethod(get_teams)
