#
#  ht_parser.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from BaseHTMLProcessor import BaseHTMLProcessor

class ht_parser(BaseHTMLProcessor):
	def reset(self):
		BaseHTMLProcessor.reset(self)

		self.__verbatim = 0
		self.__item_stack = []
		self.__content = ''
		self.__skip_item = 0

	def set_params(self, content, session):
		self.__content = content
		self.__session = session

	def unknown_starttag(self, tag, attrs):
		if self.__skip_item > 0:
			return

		BaseHTMLProcessor.unknown_starttag(self, tag, attrs)

	def unknown_endtag(self, tag):
		if self.__skip_item > 0:
			return

		BaseHTMLProcessor.unknown_endtag(self, tag)

	def handle_data(self, text):
		if self.__verbatim > 0:
			self.pieces.append(text)
			return

		if self.__skip_item > 0:
			return

		if len(self.__item_stack) == 0:
			self.pieces.append(text)
			return

		item = self.__item_stack[-1]
		item_attrs, entity, act_str = item

		import re
		import cf
		from lib.misc import txt_lang
		text = re.sub('\$text\$', '<A href="/%s/%s?%s">%s</A>' % (
				cf.ht_path, cf.ht_index,
				'&'.join(['%s=%s' % attr for attr in item_attrs]),
				txt_lang(entity.item_txt(act_str))), text)

		self.pieces.append(text)

	def start_pre(self, attrs):
		self.__verbatim += 1
		self.unknown_starttag('pre', attrs)

	def end_pre(self):
		self.unknown_endtag('pre')
		self.__verbatim -= 1

	def start_item(self, attrs):
		if self.__verbatim > 0:
			return
		
		if self.__skip_item > 0:
			self.__skip_item += 1
			return

		attr_map = dict(attrs)

		ent_str = attr_map.get('entity')
		act_str = attr_map.get('action')

		if ent_str is None or act_str is None:
			from error.error import error
			error(error.warn, 'Invalid item', 'entity: %s, action: %s' % \
					(ent_str, act_str))

		entity = self.check_item(ent_str, act_str)

		if entity is not None:
			self.__item_stack.append((attrs, entity, act_str))

	def check_item(self, ent_str, act_str):
		from erm.helper import get_entity
		entity = get_entity(ent_str, self.__session, globals())
		from erm.helper import get_action
		action = get_action(act_str, False)

		from error.error import error
		try:
			import cf
			if not cf.ht_check_items:
				from error.do_not_exec import do_not_exec
				raise do_not_exec()

			entity.accept(action)
		except error, e:
			from error.no_valid_keys import no_valid_keys
			from error.perm_denied import perm_denied

			if isinstance(e, no_valid_keys) or isinstance(e, perm_denied):
				self.__skip_item += 1
				return None
		else:
			from error.error import error
			raise error(error.error, 'action succeeded without do_exec',
				'entity: %s, action: %s' % (ent_str, act_str))

		return entity

	def end_item(self):
		if self.__verbatim > 0:
			return
		
		if self.__skip_item > 0:
			self.__skip_item -= 1
		else:
			self.__item_stack.pop()

	def do_content(self, attrs):
		self.pieces.append(self.__content)
