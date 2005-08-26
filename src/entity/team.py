#
#  team.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from erm.ent_table import *
from erm.relation import *

from txt import label
from attr.attribute import perm
from attr.string import *

class team(ent_table):
	def __init__(self):
		ent_table.__init__(self, attributes = [
			('party', string(label.party, perm.submit, '', 10)),
			('tourney', string(label.tourney, perm.submit, '', 32)),
			('name', string(label.team, perm.submit, None, 32)),
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
			cond = {	'submit':	"tn.phase = '1'" } ),
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
				'edit':		"tm.party IS NOT NULL OR leader.username = $userid" },
			outer_join = "LEFT" ),
				relation(
			table =	'team',
			alias =	'lt',
			keys = {	'party':	'party',
						'tourney':	'tourney',
						'leader':	'leader' },
						# make sure user is not a leader of another team
						# already
			cond = {	'submit':	"lt.leader IS NULL" },
			outer_join =	"LEFT" )
				],
			item_txt = {
				'edit': {
					'en':	'Team Settings',
					'de':	'Teameinstellungen' },
				'submit': {
					'en':	'Form New Team',
					'de':	'Team bilden' },
				'view': {
					'en':	'Teams' } } )
