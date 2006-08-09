#
#  entity/team.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from germ.erm.ent_table import *
from germ.erm.relation import *

from germ.txt import label
from germ.attr.attribute import perm
from germ.attr.string import *

# TODO: make 'leader' editable, but only by the leader
class team(ent_table):
	def __init__(self):
		ent_table.__init__(self, attributes = [
			('party', string(label.party, perm.all, '', 20)),
			('tourney', string(label.tourney, perm.all, '', 32)),
			('name', string(label.team, perm.all, None, 32)),
			('leader', string(label.leader, perm.all, '', 10))
			],
			primary_keys = [ 'party', 'tourney', 'name' ],
			relations = [
				relation(
			table = 'tourney',
			alias = 'tn',
			keys = {	'party':	'party',
						'tourney':	'name' },
						# make sure tournament is in preparation phase
			cond = {	'submit':	"tn.phase = '2'" } ),
				relation(
			table = 'gamer',
			keys = {	'party':	'party',
						'leader':	'username' },
			cond = {	'submit':	"gamer.username = $userid" } ),
				relation(
			table =	'users',
			alias = 'leader',
			keys = {	'leader':	'username' },
						# make sure user has paid
			cond = {	'submit':	"gamer.paid = TRUE OR leader.rank > 1" } ),
				relation(
			table = 'team_members',
			alias = 'tm',
			keys = {	'party':	'party',
						'name':		'team',
						'leader':	'username' },
			cond = {
						# ???
				'edit':	"tm.party IS NOT NULL OR leader.username = $userid" },
			outer_join = "LEFT" ),
						# make sure user is not a member of another team
			#	relation(
			#table = 'team_members',
			#alias = 'tm2',
			#keys = {	'party':	'party',
			#			'tourney':	'tourney',
			#			'leader':	'username' },
			#cond = {
			#	'edit':		"tm.party IS NOT NULL OR leader.username = $userid" },
			#outer_join = "LEFT" ),
				relation(
			table =	'team',
			alias =	'lt',
			keys = {	'party':	'party',
						'tourney':	'tourney',
						'leader':	'leader' },
						# make sure user is not a leader of another team
						# already
			cond = {	'submit':	"lt.leader IS NULL" },
			outer_join = "LEFT" ),
				relation(
			table = 'team',
			alias = 'urt',
			keys = {	'party':	'party',
						'tourney':	'tourney',
						'name':		'name' },
						# make sure user is the leader of the team
			cond = {	'edit':		"urt.leader = $userid" },
			# has to be an outer join so this relation is ignored for submit
			outer_join = "LEFT" )
				],
			item_txt = {
				'edit': {
					'en':	'Team Settings',
					'de':	'Teameinstellungen' },
				'submit': {
					'en':	'Form New Team',
					'de':	'Team bilden' },
				'view': {
					'en':	'Teams' },
				'list': {
					'en':	'Teams' } } )

	def post(self, act_str):
		if act_str == 'submit':
			leader = self._attr_map['leader'].get()
			party = self._attr_map['party'].get()
			tourney = self._attr_map['tourney'].get()
			team = self._attr_map['name'].get()

			from germ.erm.helper import sql_query

			sql_query("INSERT INTO team_members SET party = '%s', " \
					"username = '%s', tourney = '%s', team = '%s', " \
					"active = 1" % \
					(party, leader, tourney, team), self._session,
					self._globals)
