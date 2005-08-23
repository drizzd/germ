#
#  log_file_apache.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from mod_python import apache
from error import *

class log_file_apache:
	ap_log = {
		err_debug:	apache.APLOG_DEBUG,
		err_info:	apache.APLOG_INFO,
		err_notice:	apache.APLOG_NOTICE,
		err_warn:	apache.APLOG_WARNING,
		err_error:	apache.APLOG_ERR,
		err_fail:	apache.APLOG_CRIT }

	def __init__(self, req):
		self.__req = req
		
	def write(self, message, level):
		self.__req.log_error(message, log_file_apache.ap_log[level])
	
	def flush(self):
		pass
