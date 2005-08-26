#
#  db_iface.py: database interface
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

import MySQLdb
import cf

class db_iface:
	__db_type = cf.db_type
	__host = cf.db_host
	__user = cf.db_user
	__database = cf.db_database
	__password = cf.db_password
	__conn = None

	def query(cls, query):
		#from error.error import error
		#error(error.debug, 'db_iface query', query)

		if cls.__db_type == 'mysql':
			rset = cls.__sql_query_mysql(query)
		else:
			from error.error import error
			from txt import errmsg
			raise error(error.fail, errmsg.unknown_db_type,
				'db_type: %s' % db_type)

		return rset

	query = classmethod(query)

	def escape_string(cls, s):
		conn = cls.__mysql_connect()

		return conn.escape_string(s)

	escape_string = classmethod(escape_string)

	def __sql_query_mysql(cls, query):
		conn = cls.__mysql_connect()

		c = conn.cursor()
		# TODO: check for errors
		c.execute(query)

		rset = c.fetchall()
		c.close()

		return rset

	__sql_query_mysql = classmethod(__sql_query_mysql)

	def __mysql_connect(cls):
		if cls.__conn is None:
			cls.__conn = MySQLdb.connect(
				host=cls.__host,
				user=cls.__user,
				db=cls.__database,
				passwd=cls.__password)

		return cls.__conn

	__mysql_connect = classmethod(__mysql_connect)
