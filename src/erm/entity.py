#
#  entity.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

import text.errmsg
from error import *
from ref_group import *

class entity:
	def __init__(
			self, name, attributes, primary_keys,
			relations = [], perm = {}, pre = {}, post = {}):
		self.__name = name
		self._attr_vec = []
		self.__attr_map = {}
		for a in attributes:
			self.__attr_vec.append(a['name'])
			self.__attr_map[a['name']] = a['attr']

		self._pk_vec = primary_keys
		self.__rel_vec = relations
		self.__lock_map = {}

		self.__perm = perm
		self.__pre = pre
		self.__post = post

		self.__build_ref_groups()

	def perm(self, act_str):
		from lib.misc import always_true

		return self.__perm.get(act_str, always_true)()

	def pre(self, act_str):
		from lib.misc import do_nothing

		return self.__pre.get(act_str, do_nothing)()

	def post(self, act_str):
		from lib.misc import do_nothing

		return self.__post.get(act_str, do_nothing)()

	def get_name(self):
		return self.__name

	def get_pk_vec(self):
		return self._pk_vec

	def __build_ref_groups(self):
		self.__ref_group_vec = []
		for rel in self.__rel_vec:
			self.add_rel(rel)

	def add_rel(self, rel):
		join = []

		# find interdependent relations
		for idx, ref_grp in enumerate(self.__ref_group_vec):
			for key in rel.get_keys():
				if ref_grp.has_key(key):
					join.append(idx)
					break

		if len(join) > 0:
			# join reference groups
			ref_grp = self.__ref_group_vec[join[0]]

			# uh, ugly
			rev_range = range(len(join))
			rev_range.reverse()
			for i in rev_range:
				ref_grp.join(self.__ref_group_vec.pop(join[i]))
			ref_grp.add_rel(rel)
		else:
			# add new reference group
			self.__ref_group_vec.append(ref_group(rel))

# alternative implementation (untested)
#	def add_rel(self, rel):
#		i = 0
#		ref_grp_join = None
#		it = iter(self.__ref_group_vec)
#		
#		i = 0
#		for ref_grp in it:
#			for key in rel.get_keys():
#				if ref_grp.has_key(key):
#					ref_grp_join = ref_grp
#					break
#			i += 1
#			if ref_grp_join is not None
#				break
#
#		for ref_grp in it:
#			for key in rel.get_keys():
#				while ref_grp.has_key(key):
#					ref_grp_join.join(ref_grp)
#					self.__ref_group_vec.remove(i)
#					ref_grp = self.__ref_group_vec(i)
#			i += 1
#		else: ???
#			ref_grp.add_rel(rel)
#			return
#
#		# add new reference group
#		self.__ref_group_vec.append(ref_group(rel))

	def generate_keylists(self, act_str):
		for ref_grp in self.__ref_group_vec:
			ref_grp.generate_keylist(act_str, self.__attr_vec,
					self.__attr_map, self.__lock_map)
	
	def require_pk_locks(self):
		for key in self._pk_vec:
			if not self.__attr_map[key].is_locked():
				self.__lock_map[key] = None

	def accept(self, action):
		raise error(err_fail, errmsg.abstract_func)

	def get_attr(self, attr_name):
		if not self.__attr_map.has_key(attr_name):
			raise error(err_fail, errmsg.nonexisting_attr % (self.__name,
					attr_name))

		return self.__attr_map[attr_name]

	# this has to be run after each configuration change
	def init(self):
		pass
