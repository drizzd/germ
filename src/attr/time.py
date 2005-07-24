#
#  time.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from attribute import *

class time(attribute):
	def __init__(self, label, perm = {}, default = None):
		attribute.__init__(self, label, perm, default)

	def accept(self, attr_act):
		attr_act.visit_time(self)
