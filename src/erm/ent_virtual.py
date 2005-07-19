#
#  ent_virtual.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from entity import *

class ent_virtual(entity):
	def __init__(self):
		entity.__init__(self)

	def accept(self, action):
		action.visit_virtual(self)
