#
#  ui_ht/log_file.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

class log_file(file):
	def __init__(self):
		import cf
		file.__init__(self, cf.log_file_path, 'a')

	def write(self, message, level):
		from datetime import datetime
		time_str = datetime.now().strftime('%b %d %H:%M:%S')

		# TODO: add information about the user/ip this message originates from
		file.write("[%s] [%s] %s\n" % (time_str, error.lvl_txt(level), message))
