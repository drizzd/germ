#
#  attr/dummy.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from attribute import *

class dummy(attribute):
	def __init__(self):
		from germ.txt import label
		attribute.__init__(self, label = label.dummy, perm = [], default = '',
				chk_func_vec = [])

	def accept(self, attr_act):
		attr_act.visit_dummy(self)
