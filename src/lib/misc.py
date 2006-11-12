#
#  lib/misc.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

def empty():
	return []

def always_false(*args):
	return False

def always_true(*args):
	return True

def do_nothing(*args):
	pass

# Direct use of datetime.date.today as default callable doesn't work. I have no
# idea why.
def today():
	import datetime
	return datetime.date.today()

def date_str_sql(day):
	return day.strftime("%Y%m%d")

def date_str_nice(day):
	from misc import txt_lang

	format = {
		'de':	"%e. %B %Y",
		'en':	"%B %e, %Y" }

	return day.strftime(txt_lang(format))

def date_str_iso(day):
	return day.isoformat()
	#return day.strftime("%Y-%m-%d")

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

txt_lang_convert = []

def txt_lang(txt, lang = None):
	if lang is None:
		import cf
		lang = cf.lang

	text = txt.get(lang, txt['en'])

	for conv in txt_lang_convert:
		text = conv(text)

	return text

class var_check:
	def __init__(self, entity, var, val):
		self.__entity = entity
		self.__var = var
		self.__val = val

	def __call__(self):
		return self.__entity.get_var(self.__var) == self.__val

def get_cond(cond, act_str):
	if not isinstance(cond, dict):
		from germ.error.error import error
		raise error(error.error, 'Invalid condition type',
				'cond: %s, type: %s' % (cond, type(cond)))

	cond_act = cond.get(act_str)
	cond_all = cond.get('all')

	if cond_act is None:
		return cond_all
	elif cond_all is None:
		return cond_act
	else:
		return '(%s) AND (%s)' % (cond_all, cond_act)

def call_if(expr, *args):
	if callable(expr):
		return expr(*args)
	else:
		return expr
