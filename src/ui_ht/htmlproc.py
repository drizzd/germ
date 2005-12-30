#
#  htmlproc.py
#
#  Copyright (C) 2005 Clemens Buchacher <@>
#

from HTMLParser import HTMLParser

class htmlproc(HTMLParser):
	def reset(self):
		self.__output = ''
		self._data = ''
		self.__parse = None
		self.__parse_tag = None
		self.__parse_depth = 0

		HTMLParser.reset(self)

	def handle_tag(self, text, style, tag, attrs = None):
		try:
			handler = getattr(self, style + '_' + tag)
		except AttributeError:
			self.handle_data(text)
		else:
			if attrs:
				text = handler(tag, attrs)
			else:
				text = handler(tag)

			if text:
				self._data += text

	def handle_starttag(self, tag, attrs):
		text = self.get_starttag_text()

		if self.__parse_depth > 0:
			if tag != self.__parse_tag:
				self.handle_data(text)
				return
			else:
				self.__parse_depth += 1
		else:
			try:
				parse = getattr(self, 'parse_' + tag)
			except AttributeError:
				pass
			else:
				self.__consume()

				self.__parse_tag = tag
				self.__parse_depth = 1
				self.__parse = parse

		self.handle_tag(text, 'start', tag, attrs)

	def handle_startendtag(self, tag, attrs):
		text = self.get_starttag_text()

		if self.__parse_depth > 0:
			self.handle_data(text)
			return

		self.handle_tag(text, 'startend', tag, attrs)

	def handle_endtag(self, tag):
		text = '</%s>' % tag

		if self.__parse_depth > 0:
			if tag != self.__parse_tag:
				self.handle_data(text)
				return
			else:
				self.__consume()

				self.__parse_depth -= 1

		self.handle_tag(text, 'end', tag)

	def handle_charref(self, name):
		self.handle_data('&#%s;' % name)

	def handle_entityref(self, name):
		self.handle_data('&%s' % name)

		import htmlentitydefs
		if htmlentitydefs.entitydefs.has_key(ref):
			self.handle_data(';')

	def handle_decl(self, decl):
		self.handle_data('<!%s>' % decl)

	def handle_pi(self, data):
		self.handle_data('<?%s>' % data)

	def handle_comment(self, comment):
		self.__consume()
		self.__output += '<!--%s-->' % comment

	def output(self):
		HTMLParser.close(self)

		if self.__parse_depth != 0:
			raise 'unmatched tag (%s)' % self.__parse_tag

		self.__consume()

		return self.__output

	def handle_data(self, data):
		self._data += data

	def __consume(self):
		if self.__parse_depth > 0:
			self.__parse()

		self.__output += self._data
		self._data = ''
