#
#  ui_ht/ht_parser.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from htmlproc import htmlproc

class ht_parser(htmlproc):
	def reset(self):
		htmlproc.reset(self)

		self._hide = 0
		self.__item_stack = []

		self._content = ''
		self._session = {}

	def set_params(self, content, session):
		self._content = content
		self._session = session

	def parse_pre(self):
		pass

	def start_item(self, attrs):
		if self._hide > 0:
			self._hide += 1
			return

		attr_map = dict(attrs)

		ent_str = attr_map.get('entity')
		act_str = attr_map.get('action')

		if ent_str is None or act_str is None:
			from germ.error.error import error
			raise error(error.warn, 'Invalid item', 'entity: %s, action: %s' \
					% (ent_str, act_str))

		entity = self.__check_item(ent_str, act_str)

		for k in attr_map:
			import re

			attr_map[k] = re.sub(r'\$([A-Za-z_][A-Za-z0-9_]*)',
					self.__variable, attr_map[k])

		if entity is not None:
			self.__item_stack.append((attr_map, entity, act_str))

	def parse_item(self):
		if self._hide > 0:
			self._data = ''
			return

		if len(self.__item_stack) == 0:
			return

		item = self.__item_stack[-1]
		attrs, entity, act_str = item

		import re
		import cf
		from germ.lib.misc import txt_lang
		self._data = re.sub('\$text\$', '<A href="%s?%s">%s</A>' % (
				cf.ht_index, '&'.join(['%s=%s' % attr for attr in
					attrs.iteritems()]),
				txt_lang(entity.item_txt(act_str))), self._data)

	def end_item(self):
		if self._hide > 0:
			self._hide -= 1
		else:
			self.__item_stack.pop()

	def startend_content(self, attrs):
		return self._content

	def __check_item(self, ent_str, act_str):
		from germ.erm.helper import get_entity
		entity = get_entity(ent_str, self._session, globals())
		from germ.erm.helper import get_action
		action = get_action(act_str, False)

		from germ.error.error import error
		try:
			import cf
			if not cf.ht_check_items:
				from germ.error.do_not_exec import do_not_exec
				raise do_not_exec()

			entity.accept(action)
		except error, e:
			from germ.error.no_valid_keys import no_valid_keys
			from germ.error.perm_denied import perm_denied
			from germ.error.do_not_exec import do_not_exec

			if isinstance(e, no_valid_keys) or isinstance(e, perm_denied):
				self._hide += 1
				return None
			elif not isinstance(e, do_not_exec):#elif e.lvl() > error.notice:
				import sys
				exctype, exc, tb = sys.exc_info()
				raise exctype, exc, tb
		else:
			raise error(error.error, 'action succeeded without do_exec',
				'entity: %s, action: %s' % (ent_str, act_str))

		return entity

	def __variable(self, match):
		varname = match.group(1)

		if not self._session.has_key(varname):
			return ''

		val = self._session[varname]

		if not isinstance(val, str):
			from germ.error.error import error
			raise error(error.fail, "Session variables for use in a " \
					"URL must be strings",
					"variable: %s, type: %s" % (varname, type(val)))

		import urllib

		return urllib.quote_plus(val, '')
