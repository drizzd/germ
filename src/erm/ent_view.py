#
#  erm/ent_view.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from entity import *

class ent_view(entity):
	def __init__(self):
		entity.__init__(self)

	def accept(self, action):
		action.visit_view(self)
