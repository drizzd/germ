#
#  entity/gamer.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from germ.erm.ent_table import *
from germ.erm.relation import *

from germ.txt import label
from germ.attr.attribute import perm
from germ.attr.string import *
from germ.attr.int import *
from germ.attr.bool import *

# TODO: make sure user can not change the 'paid' field
class gamer(ent_table):
	def __init__(self):
		from users import rank_check

		perm_paid = {
				'view': True,
				'edit': rank_check(self, 2) }

		from germ.lib.chk import greater_equal

		ent_table.__init__(self, attributes = [
			('party', string(label.party, perm.all + ['delete'], '', 20)),
			('username', string(label.username, perm.all + ['delete'], '', 10)),
			('seat', int(label.seat, perm.edit, 0, 8, [greater_equal(0)])),
			('paid', bool(label.paid, perm_paid, 0))
			],
			primary_keys = [ 'party', 'username' ],
			relations = [
				relation(
			table =	'users',
			keys = {	'username':	'username' },
			cond = {
				'edit':
					"(users.username = $userid AND " \
						# make sure user has paid
						"(gamer.paid = 1 OR $users.rank > 1)) OR " \
					"($users.rank > 1 AND users.rank < $users.rank)",
				'submit':
					"users.username = $userid OR " \
					"($users.rank > 1 AND users.rank < $users.rank)",
				'delete':
					# The 'gamer.paid = 0' condition should make sure that the
					# gamer is not subscribed to any tournaments yet, so that
					# cancelling the registration does not violate any
					# dependencies. Cancelling a registration after the gamer
					# has paid requires special considerations.
					"(users.username = $userid OR " \
					"($users.rank > 1 AND users.rank < $users.rank)) " \
					"AND gamer.paid = 0" }),
				relation(
			table =	'party',
			keys = {	'party':	'name' },
			cond = {		# party has to be in registration phase
				'submit':	"party.status = 1 OR $users.rank > 1",
				'edit':		"party.status = 1 OR $users.rank > 1" }),
			# Ok, I don't think this will work. We could handle this with
			# dynamic permissions though. That way, the user will be able to
			# enter the edit form, even if he can't change anything.
#				relation(
#			table = 'gamer',
#			alias = 'haspaid',
#			keys = {	'party':	'party',
#						'username':	'username' },
#			cond = {	# make sure user can not change the 'paid' field
#				'edit':	"$users.rank > 1 OR gamer.paid = haspaid.paid" },
#			# has to be an outer join so this relation is ignored for submit
#			outer_join = "LEFT"),
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

#	def check_rank(self, attrs):
#		from germ.erm.helper import get_entity
#		e = get_entity('users', self._session, self._globals)
#
#		e.substitute_attr('username', self._attr_map['username'])
#
#		return e.check_rank(attrs)
