#
#  gamer.py
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
		ent_table.__init__(self, attributes = [
			('party', string(label.party, perm.submit, None, 10)),
			('username', string(label.username, perm.submit, None, 10)),
			('seat', int(label.seat, perm.edit, 0)),
			('paid', bool(label.paid, perm.view, 0))
			],
			primary_keys = [ 'party', 'username' ],
			relations = [
				relation(
			table =	'users',
			keys = {	'username':	'username' },
			cond = "users.username = '$userid'" ),
				relation(
			table =	'party',
			keys = {	'party':		'name' },
			# party has to be in registration phase
			cond = {
				'submit':	'party.status = 1 OR users.rank > 1',
				'edit':		'(party.status = 1 AND gamer.paid = 1) ' \
							'OR users.rank > 1'})
				],
			item_txt = {
				'edit': {
					'en': 'My Parties',
					'de': 'Meine Anmeldung' },
				'submit': {
					'en': 'Join Party',
					'de': 'Anmeldung' },
				'delete': {
					'en': 'Cancel Party',
					'de': 'Abmeldung' } },
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
