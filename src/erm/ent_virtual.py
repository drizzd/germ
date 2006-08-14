#
#  erm/ent_virtual.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from entity import *

class ent_virtual(entity):
	from germ.txt import misc

	def __init__(self, attributes, primary_keys, relations = [],
			item_txt = {}, action_txt = misc.action,
			action_report = misc.action_report, perm = {}, pre = {},
			post = {}, magic_var = {}):
		args = vars()
		del args['self']
		entity.__init__(self, **args)

	def do_accept(self, action):
		action.visit_virtual(self)
