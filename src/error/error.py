#
#  error.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

class error(Exception):
	log_file = None
	debug, info, notice, warn, error, fail = range(0,6)

	def __init__(self, lvl, msg, add_info = None, do_log = True):
		self.__lvl = lvl
		self.__msg = msg
		self.__add_info = add_info

		if do_log:
			self.log()

	def log(self):
		if self.log_file is None:
			return

		for line in str(self).split('\n'):
			self.log_file.write(line, self.__lvl)

		self.log_file.flush()

	def __str__(self):
		from lib import misc

		msg = isinstance(self.__msg, dict) and \
				misc.txt_lang(self.__msg) or self.__msg

		if self.__add_info is None:
			add_info = ''
		else:
			add_info = ' (%s)' % self.__add_info

		return "%s%s" % (msg, add_info)

	def __repr__(self):
		return self.__str__()

	def lvl(self):
		return self.__lvl

	def lvl_txt(level):
		from txt.errmsg import error_lvl
		from lib import misc

		return misc.txt_lang(error_lvl[level])
	lvl_txt = staticmethod(lvl_txt)
