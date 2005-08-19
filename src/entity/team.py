#
#  team.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from erm.ent_table import *
import txt.label
from erm.relation import *

from attr.attribute import perm
from attr.string import *

class team(ent_table):
	def __init__(self):
		ent_table.__init__(self, attributes = [
			('party', string(label.party, perm.submit, None, 10)),
			('tourney', string(label.tourney, perm.submit, None, 32)),
			('name', string(label.teamname, perm.submit, None, 32)),
			('leader', string(label.leader, perm.submit, None, 10)),
			],
			primary_keys = [ 'party', 'tourney', 'name' ],
			relations = [
				relation(
			table = 'tourney',
			alias = 'tn',
			keys = {	'party':	'party',
						'name':		'tourney' },
						# make sure tournament is in preparation phase
			cond = {	'submit':	"tn.phase = '2'",
						'edit':		"tn.phase = '2'" } ),
				relation(
			table = 'gamer',
			keys = {	'party':	'party',
						'username':	'leader' },
			cond = {	'submit':	"gamer.username = '$userid'" } ),
				relation(
			table =	'users',
			keys = {	'username':		'leader' },
						# make sure user has paid
			cond = {	'submit':	"gamer.paid = TRUE OR users.rank > 1" } ),
				relation(
			table =	'team',
			alias =	'lt',
			keys = {	'party':	'party',
						'tourney':	'tourney',
						'leader':	'leader' },
						# make sure user is not a leader of another team
						# already
			cond = {	'submit':	"lt.leader IS NULL OR team.name = lt.name",
						'edit':		"lt.leader IS NULL OR team.name = lt.name"
					},
			outer_join =	"LEFT" )
				])
