#
#  error.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

err_debug, err_note, err_warn, err_error, err_fail = range(0,5)

class error(Exception):
	try:
		log_file = file(log_file_path)
	except IOError:
		# Cannot log to a file and cannot inform the user. Otherwise the
		# user could gather information about the system we don't want him
		# to know.
		pass

	def __init__(self, lvl, msg, add_info = None, do_log = True):
		self.__lvl = lvl
		self.__msg = msg
		self.__add_info = add_info

		if do_log:
			self.__log()

	def __log(self):
		from datetime import datetime

		time_str = datetime.now().strftime('%b %d %H:%M:%S')

		# TODO: add information about the user/ip this message originates from
		error.log_file.write("%s %s" % (time_str, self))
		error.log_file.flush()

	def __str__(self):
		import cf

		msg = isinstance(self.__msg, list) and
			self.__msg[cf.lang] or self.__msg

		from text.errmsg import error_lvl

		return "%s: %s%s" % (error_lvl[self.__lvl][cf.lang], msg,
			self.__add_info is None and '' or ' (' + self.__add_info + ')')

	def __repr__(self):
		return self.__str__()
