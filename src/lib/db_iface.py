#
#  db_iface.py: database interface
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

import MySQLdb
import cf
from error import *

class db_iface:
	type = cf.db_type
	host = cf.db_host
	user = cf.db_user
	database = cf.db_database
	password = cf.db_password

	def sql_query(cls, query):
		if type == 'mysql':
			res = db_iface.sql_query_mysql(query)
		else:
			raise error(err_fail, 'Unkown database type: %s' % type)

		return res

	sql_query = classmethod(sql_query)

	def sql_query_mysql(cls, query):
		cls.mysql_connect()

		c = cls.conn.cursor()
		c.execute(query)
		res = c.fetchall()
		c.close()

		return res

	sql_query_mysql = classmethod(sql_query_mysql)

	def mysql_connect(cls):
		if not isinstance(cls.conn, Connection):
			cls.conn = MySQLdb.connect(
				host=cls.host,
				user=cls.user,
				db=cls.database,
				passwd=cls.password)

	mysql_connect = classmethod(mysql_connect)
