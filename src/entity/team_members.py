#
#  team_members.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from erm.ent_table import *
import text.label
from erm.relation import *

from attr.attribute import perm
from attr.string import *

class team_members(ent_table):
	def __init__(self):
		ent_table.__init__(self, name = __name__, attributes = [
			('party', string(label.party, perm.submit, None, 10)),
			('username', string(label.username, perm.submit, None, 10)),
			('tourney', string(label.tourney, perm.submit, None, 32)),
			('team', string(label.team, perm.all, None, 32))
			],
			primary_keys = [ 'party', 'username', 'tourney' ],
			relations = [
				relation(
			table =	'gamer',
			keys =	{ 'party':		'party',
		  			  'username':	'username' },
			cond =	{ 'submit':	"gamer.username = '$userid'" } ),
				relation(
			table =	'team',
			keys =	{ 'party':		'party',
		  			  'tourney':	'tourney',
		  			  'team':		'name' },
			cond =	{ 'edit':	"team.leader = '$userid'" } ),
				relation(
			table =	'tourney',
			alias =	'tn',
			keys =	{ 'party':		'party',
		  			  'tourney':	'name' },
			cond =	{ 'submit':	"tn.phase = '2'",
		  			  'edit':	"tn.phase = '2'" } ),
				relation(
			table =	'users',
			keys =	{ 'username':		'username' },
			cond =	{ 'submit':	"gamer.paid = TRUE OR users.rank > 1" } ),
				relation(
			table =	'team',
			alias =	'lt',
			keys =	{ 'party':		'party',
		  			  'tourney':	'tourney',
		  			  'username':	'leader' },
			cond =	{ 'submit':	"lt.leader IS NULL OR team.name = lt.name" },
			outer_join =	"LEFT" )
				])
