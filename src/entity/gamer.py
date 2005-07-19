#
#  gamer.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from erm.ent_table import *
import text.label
from attribute.string import *
from erm.relation import *

from erm.attribute import *

class gamer(ent_table):
	def __init__(self):
		ent_table.__init__(self, name = __name__, attributes = [
			init('party', string(label.party, perm.submit, None, 10)),
			init('username', string(label.username, perm.submit, None, 10)),
			init('seat', int(label.tourney, perm.edit)),
			init('paid', bool(label.team, perm.view, 0))
			],
			primary_keys = [ 'party', 'username' ],
			relations = [
				relation(
			table =	'users',
			keys =	{ 'username':	'username' },
			cond =	{ 'submit':	"users.username = '$userid'" } ),
				relation(
			table =	'party',
			keys =	{ 'party':		'name' },
			# party has to be in registration phase
			cond =	{ 'submit':	"party.status = 1 OR users.rank > 1" } )
				])
