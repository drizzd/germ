#
#  ent_virtual.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from entity import *

class ent_virtual(entity):
	from txt import misc

	def __init__(self, attributes, primary_keys, relations = [],
			condition = {}, item_txt = {}, action_txt = misc.action,
			action_report = misc.action_report, perm = {}, pre = {},
			post = {}):
		entity.__init__(self, attributes, primary_keys, relations, condition,
				item_txt, action_txt, action_report, perm, pre, post)

	def do_accept(self, action):
		action.visit_virtual(self)
