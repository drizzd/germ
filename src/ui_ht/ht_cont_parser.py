#
#  ui_ht/ht_cont_parser.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from ht_parser import ht_parser

# TODO: maybe unite this with ht_parser
class ht_cont_parser(ht_parser):
	def reset(self):
		ht_parser.reset(self)

		self.__print_parm = None
		self.__done = False
		self.__entity = None

	def startend_content(self, attrs):
		self.__done = True

		from print_handlers import do_print

		return do_print(**self.__print_parm)

	def set_params(self, session, print_parm):
		ht_parser.set_params(self, 'asdf', session)

		self.__print_parm = print_parm
		self.__entity = print_parm['entity']

	def start_list(self, attrs):
		if self._hide > 0 or not self.__entity.has_rset():
			self._hide += 1

	def parse_list(self):
		if self._hide > 0:
			self._data = ''
			return

		self.__done = True

		text = ''

		from ht_list_parser import ht_list_parser

		parser = ht_list_parser()

		for rec in self.__entity.rsets('view'):
			parser.reset()
			parser.set_params(self._content, self._session, rec)
			parser.feed(self._data)

			text += parser.output()

		self._data = text

	def end_list(self):
		if self._hide > 0:
			self._hide -= 1

	def output(self):
		if not self.__done:
			self._data += self.startend_content([])

		return ht_parser.output(self)
