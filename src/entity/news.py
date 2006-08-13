#
#  entity/news.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from germ.erm.ent_table import *
from germ.erm.relation import *

from germ.txt import label
from germ.attr.attribute import perm
from germ.attr.sql_id import *
from germ.attr.string import *
from germ.attr.date import *
from germ.attr.text import *

class news(ent_table):
	def __init__(self):
		from germ.lib.chk import greater_equal

		ent_table.__init__(self, attributes = [
			('id', sql_id(label.id, perm.edit)),
			('username', string(label.username, perm.all, '', 10)),
			('date', date(label.date, perm.submit + ['list'])),
			('content', text(label.content, perm.all))
			],
			primary_keys = [ 'id' ],
			relations = [
				relation(
			table =	'users',
			keys = {	'username':	'username' },
			cond = {
				'edit':
					"users.username = $userid OR $users.rank > users.rank",
				'submit':
					"users.username = $userid AND $users.rank > 0",
				'delete':
					"users.username = $userid OR $users.rank > users.rank" }),
				],
			item_txt = {
				'edit': {
					'en': 'Edit news',
					'de': 'News editieren' },
				'submit': {
					'en': 'Post news',
					'de': 'News erstellen' },
				'delete': {
					'en': 'Delete news',
					'de': 'News l"oschen' },
				'view': {
					'en': 'News' },
				'list': {
					'en': 'News' } },
			action_txt = {
				'submit': {
					'en': 'post',
					'de': 'erstellen' },
				'delete': {
					'en': 'delete',
					'de': 'l"oschen' } },
			action_report = {
				'submit': {
					'en': 'The news have been posted',
					'de': 'Die News wurden erstellt' },
				'delete': {
					'en': 'The news have been deleted',
					'de': 'Die News wurden gel"oscht' } })
