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

# same as [i for i in a_vec if i not in b_vec]
# which is faster?
def vec_sub(a_vec, b_vec):
	a_vec = a_vec[:]
	b_vec = b_vec[:]

	a_len = len(a_vec)
	b_len = len(b_vec)
	i = 0
	while i < a_len && pk_len > 0:
		a = a_vec[i]

		if a not in b_vec:
			i++
		else:
			b_vec.remove(a)
			b_len--
			attr_vec.pop(i)
			a_len--

	return a_vec

# if len(b_vec) is very small:
def vec_sub_small(a_vec, b_vec):
	a_vec = a_vec[:]

	a_len = len(a_vec)
	b_len = len(b_vec)
	i = 0
	while i < a_len && pk_len > 0:
		a = a_vec[i]

		if a not in b_vec:
			i++
		else:
			attr_vec.pop(i)
			a_len--

	return a_vec
