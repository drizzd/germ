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
		#from users import rank_check

		#perm_paid = {
		#		'view': True,
		#		'edit': rank_check(self, 1) }
		perm_paid = {
				'view': True,
				'edit': self.perm_paid }

		perm_seat = {
				'edit': self.perm_seat }

		from germ.lib.chk import greater_equal

		ent_table.__init__(self, attributes = [
			('party', string(label.party, perm.all + ['delete'], '', 20)),
			('username', string(label.username, perm.all + ['delete'], '', 10)),
			('seat', int(label.seat, perm_seat, 0, 8, [greater_equal(0)])),
			('paid', bool(label.paid, perm_paid, 0))
			],
			primary_keys = [ 'party', 'username' ],
			relations = [
				relation(
			table =	'users',
			keys = {	'username':	'username' },
			cond = {
				'edit':
					"users.username = $userid OR " \
					"users.rank < $users.rank",
					#"(users.username = $userid AND " \
					#	# make sure user has paid
					#	"(gamer.paid = TRUE OR $users.rank > 0)) OR " \
					#"users.rank < $users.rank",
				'submit':
					"users.username = $userid OR users.rank < $users.rank",
				'delete':
					# The 'gamer.paid = 0' condition should make sure that the
					# gamer is not subscribed to any tournaments yet, so that
					# cancelling the registration does not violate any
					# dependencies. Cancelling a registration after the gamer
					# has paid requires special considerations.
					"(users.username = $userid OR users.rank < $users.rank) " \
					"AND gamer.paid = FALSE" }),
				relation(
			table =	'party',
			keys = {	'party':	'name' },
			cond = {
				# party has to be in registration phase or
				# running phase
				'submit':	"party.status IN (1, 2)",
				'edit':		"party.status IN (1, 2)" }),
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
					'de': 'Spieler' },
				'list': {
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

	def perm_paid(self, attrs):
		if not self.pks_locked():
			return True

		if self.has_paid():
			return False

		from users import rank_check

		if rank_check(self, 1)():
			return True

	def perm_seat(self, attrs):
		if not self.pks_locked():
			return True

		return self.has_paid()

	def has_paid(self):
		# TODO: This is very similar to ent_table.get_rec().

		from germ.erm.helper import sql_query

		rset = sql_query("SELECT paid FROM %s WHERE %s" % \
				(self._name, self.get_attr_sql_pk()), self._session,
				self._globals)

		if len(rset) != 1:
			from germ.error.error import error
			raise error(error.fail, "Invalid primary key: result is empty " + \
					"or has multiple records", "number of records: %s" % \
					len(rset))

		return rset[0][0] == 1

#	def check_rank(self, attrs):
#		from germ.erm.helper import get_entity
#		e = get_entity('users', self._session, self._globals)
#
#		e.substitute_attr('username', self._attr_map['username'])
#
#		return e.check_rank(attrs)
