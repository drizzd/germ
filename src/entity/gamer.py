#
#  entity/gamer.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from erm.ent_table import *
from erm.relation import *

from txt import label
from attr.attribute import perm
from attr.string import *
from attr.int import *
from attr.bool import *

class gamer(ent_table):
	def __init__(self):
		from lib.chk import greater_equal

		ent_table.__init__(self, attributes = [
			('party', string(label.party, perm.submit, '', 10)),
			('username', string(label.username, perm.submit, '', 10)),
			('seat', int(label.seat, perm.edit, 0, 8, [greater_equal(0)])),
			('paid', bool(label.paid, perm.edit, 0))
			],
			primary_keys = [ 'party', 'username' ],
			relations = [
				relation(
			table =	'users',
			keys = {	'username':	'username' },
			cond = {
				'edit':
					"(users.username = $userid AND " \
						"(gamer.paid = 1 OR $users.rank > 1)) OR " \
					"($users.rank > 1 AND users.rank < $users.rank)",
				'submit':
					"users.username = $userid OR " \
					"($users.rank > 1 AND users.rank < $users.rank)",
				'delete':
					"users.username = $userid OR " \
					"($users.rank > 1 AND users.rank < $users.rank)" }),
				relation(
			table =	'party',
			keys = {	'party':	'name' },
			cond = {		# party has to be in registration phase
				'submit':	"party.status = 1 OR $users.rank > 1",
				'edit':		"party.status = 1 OR $users.rank > 1" }),
				relation(
			table = 'gamer',
			alias = 'haspaid',
			keys = {	'party':	'party',
						'username':	'username' },
			cond = {	# make sure user can not change the 'paid' field
				'edit':	"$users.rank > 1 OR gamer.paid = haspaid.paid" }),
				relation(
			table = 'gamer',
			alias = 'seats',
			keys = {	'seat':	'seat' },
			cond = {	'edit':	"seats.seat IS NULL OR seats.seat = '0'"	},
			outer_join = "LEFT")
				],
			item_txt = {
				'edit': {
					'en': 'Joined Parties',
					'de': 'Anmeldung' },
				'submit': {
					'en': 'Join Party',
					'de': 'Anmelden' },
				'delete': {
					'en': 'Cancel Party',
					'de': 'Abmelden' },
				'view': {
					'en': 'Gamers',
					'de': 'Spieler' } },
			action_txt = {
				'submit': {
					'en': 'register',
					'de': 'anmelden' },
				'delete': {
					'en': 'unregister',
					'de': 'abmelden' } },
			action_report = {
				'submit': {
					'en': 'Your party registration has been submitted',
					'de': 'Ihre Anmeldung wurde aufgenommen' },
				'delete': {
					'en': 'You have cancelled your party registration',
					'de': 'Sie sind abgemeldet' } })
