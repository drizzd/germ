#
#  attr/sql_id.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from attribute import *
from germ.txt import label

class sql_id(attribute):
	def __init__(self, label = label.sql_id, perm = []):
		attribute.__init__(self, label, perm, None, [])

	def _sql_str(self):
		return str(self._val)

	def sql_type(self):
		return 'MEDIUMINT NOT NULL AUTO_INCREMENT'

	def _do_set(self, val):
		try:
			self._val = int(val)
		except ValueError, e:
			self._error(e)

	def accept(self, attr_act):
		attr_act.visit_sql_id(self)
