#
#  ent_virtual.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from entity import *

class ent_virtual(entity):
	def __init__(self, attributes, primary_keys, relations = [],
			condition = {}, perm = {},
			pre = {}, post = {}):
		entity.__init__(self, attributes, primary_keys, relations, condition,
				perm, pre, post)

	def accept(self, action):
		action.visit_virtual(self)
