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

def date_sqlstr(day):
	return day.strftime("%Y%m%d")

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
