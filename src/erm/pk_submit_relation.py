#
#  erm/pk_submit_relation.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from relation import *

# TODO: fix this comment
# This class is currently unused for the reason described below
class pk_submit_relation(relation):
	def __init__(
			self, table, keys,
			alias = None, cond = None, outer_join = None):
		relation.__init__(self, table, keys, alias, cond, outer_join)
