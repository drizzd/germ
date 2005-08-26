#
#  entity/team_members.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from erm.ent_table import ent_table
from erm.relation import relation

from txt import label
from attr.attribute import perm
from attr.string import string
from attr.bool import bool

class team_members(ent_table):
	def __init__(self):
		ent_table.__init__(self, attributes = [
			('party', string(label.party, perm.submit, '', 10)),
			('username', string(label.username, perm.submit, '', 10)),
			('tourney', string(label.tourney, perm.submit, '', 32)),
			('team', string(label.team, perm.submit, '', 32)),
			('active', bool(label.active, perm.edit, 0))
			],
			primary_keys = [ 'party', 'username', 'tourney' ],
			relations = [
				relation(
			table =	'gamer',
			keys = {	'party':		'party',
						'username':	'username' },
						# users can only subscribe themselves
			cond = {	'submit':	"gamer.username = $userid" } ),
				relation(
			table =	'team',
			keys = {	'party':	'party',
						'tourney':	'tourney',
						'team':		'name' },
						# only the team leader can change member settings
			cond = {	'edit':		"team.leader = $userid" } ),
				relation(
			table =	'tourney',
			alias =	'tn',
			keys = {	'party':		'party',
						'tourney':	'name' },
						# make sure tournament is in preparation phase
			cond = {	'submit':	"tn.phase = '1'",
						'edit':		"tn.phase = '1'" } ),
				relation(
			table =	'users',
			keys = {	'username':		'username' },
						# make sure user has paid
			cond = {	'submit':	"gamer.paid = TRUE OR users.rank > 1" } ),
				relation(
			table =	'team',
			alias =	'lt',
			keys = {	'party':	'party',
						'tourney':	'tourney',
						'username':	'leader' },
						# make sure user is not a leader of another team
						# already
			cond = {	'submit':	"lt.leader IS NULL OR team.name = lt.name" },
			outer_join =	"LEFT" )
				],
			item_txt = {
				'edit': {
					'en': 'Teammember Settings',
					'de': 'Teammitglieder Einstellengen' },
				'submit': {
					'en': 'Join Team',
					'de': 'Team beitreten' },
				'view': {
					'en': 'Teammembers',
					'de': 'Teammitglieder' } } )
