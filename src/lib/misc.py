#
#  misc.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

def empty():
	return []

def always_false():
	return False

def always_true():
	return True

def do_nothing():
	pass

# Direct use of datetime.date.today as default callable doesn't work. I have no
# idea why.
def today():
	import datetime
	return datetime.date.today()

def date_str_sql(day):
	return day.strftime("%Y%m%d")

def date_str_nice(day):
	from lib import misc

	format = {
		'de':	"%e. %B %Y",
		'en':	"%B %e, %Y" }

	return day.strftime(misc.txt_lang(format))

def date_str_iso(day):
	return day.strftime("%Y-%m-%d")

# same as [i for i in a_vec if i not in b_vec]
# or list(Set(a) - Set(b))
# which is faster?
def vec_sub(a, b):
	a = a[:]
	from sets import Set
	b = Set(b)

	i = 0
	while i < len(a):
		if a[i] in b:
			a.pop(i)
		else:
			i += 1

	return a

def txt_lang(txt):
	import cf

	return txt.get(cf.lang, txt['en'])

class var_check:
	def __init__(self, entity, var, val):
		self.__entity = entity
		self.__var = var
		self.__val = val

	def __call__(self):
		return self.__entity.get_var(self.__var) == self.__val

class rank_check:
	def __init__(self, entity, rank):
		self.__entity = entity
		self.__rank = rank

	def __call__(self):
		userid = self.__entity.get_var('userid')

		if userid is None:
			return False

		from lib.db_iface import db_iface

		rset = db_iface.query("SELECT rank FROM users WHERE username = '%s'" \
				% userid)

		if len(rset) != 1:
			from error import *
			raise error(err_fail, "Invalid userid", 'userid: %s' % userid)

		rec = rset[0]

		return int(rec[0]) >= self.__rank
