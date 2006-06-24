#
#  ui_ht/ht_list_parser.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from ht_parser import ht_parser

class ht_list_parser(ht_parser):
	def reset(self):
		ht_parser.reset(self)

		self.__rec = None

	def set_params(self, content, session, rec):
		ht_parser.set_params(self, content, session)

		self.__rec = rec

	def startend_attr(self, attrs):
		attr_map = dict(attrs)

		name = attr_map.get('name')

		if name is None:
			from germ.error.error import error
			raise error(error.warn, 'Invalid attr tag', 'name: %s' % (name))

		attr = self.__rec.get_attr(name, 'view')

		from attr_act_view import attr_act_view
		act_view = attr_act_view()

		attr.accept(act_view)
		return act_view.get_text()
