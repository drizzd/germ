#
#  ui_ht/log_file_apache.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from mod_python import apache

class log_file_apache:
	from germ.error.error import error

	ap_log = {
		error.debug:	apache.APLOG_DEBUG,
		error.info:	apache.APLOG_INFO,
		error.notice:	apache.APLOG_NOTICE,
		error.warn:	apache.APLOG_WARNING,
		error.error:	apache.APLOG_ERR,
		error.fail:	apache.APLOG_CRIT }

	def __init__(self, req):
		self.__req = req
		
	def write(self, message, level):
		self.__req.log_error(message, log_file_apache.ap_log[level])
	
	def flush(self):
		pass
