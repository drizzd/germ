#
#  error.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

err_debug, err_info, err_notice, err_warn, err_error, err_fail = range(0,6)

class error(Exception):
	import cf
	log_file = file(cf.log_file_path, 'a')

	def __init__(self, lvl, msg, add_info = None, do_log = True):
		self.__lvl = lvl
		self.__msg = msg
		self.__add_info = add_info

		if do_log:
			self.__log()

	def err_lvl(self):
		from txt import errmsg
		error_lvl = errmsg.error_lvl[self.__lvl]
		import cf

		return error_lvl.get(cf.lang, error_lvl.get('en'))

	def __log(self):
		from datetime import datetime
		time_str = datetime.now().strftime('%b %d %H:%M:%S')

		# TODO: add information about the user/ip this message originates from
		for line in str(self).split('\n'):
			error.log_file.write("%s %s: %s\n" % (time_str, self.err_lvl(),
					line))

		error.log_file.flush()

	def __str__(self):
		import cf

		msg = isinstance(self.__msg, dict) and \
				self.__msg[cf.lang] or self.__msg

		if self.__add_info is None:
			add_info = ''
		else:
			add_info = ' (%s)' % self.__add_info

		return "%s%s" % (msg, add_info)

	def __repr__(self):
		return self.__str__()
