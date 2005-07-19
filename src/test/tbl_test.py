#
#  tbl_test.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from erm.ent_table import *
import text.label

class tbl_test(ent_table):
	def __init__(self):
		ent_table.__init__(self)

		self.__add_attr([
		{ 'name': 'username', 'label': label.username,
		  'attr': attr_string(
		      perm = { 'view': true, 'edit': false, 'submit': true },
		      length = 10),
		  'pk': true },
		{ 'name': 'address', 'label': label.address,
		  'attr': attr_string(
		      perm = { 'view': true, 'edit': true, 'submit': true },
		      length = 30) },
		{ 'name': 'dateofbirth', 'label': label.dateofbirth,
		  'attr': attr_date({ 'view': false, 'edit': false, 'submit': true }) }
		])

		self.__add_rel([
		{ 'table': gamer,
		  'keys': { 'party': party, 'nick': nick },
		  'cond': "gamer.nick = '$userid'" },
		{ 'table': 

