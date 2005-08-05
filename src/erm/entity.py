#
#  entity.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from error.error import *
from text import errmsg

from ref_group import *

class entity:
	def __init__(
			self, name, attributes, primary_keys,
			relations = [], perm = {}, pre = {}, post = {}):
		self._name = name
		self._attr_vec = []
		self._attr_map = dict(attributes)
		for a in attributes:
			self._attr_vec.append(a[0])

		self.__rset = None

		self._pk_vec = primary_keys
		self.__rel_vec = relations
		self.__lock_map = {}

		self.__perm = perm
		self.__pre = pre
		self.__post = post

		self.__build_ref_groups()

	def set_rset(self, rset):
		if self.__rset is not None:
			raise error(err_fail, "Attempt to set result set twice",
				"entity: %s" % self._name)

		self.__rset = rset

	def has_rset(self):
		return self.__rset is not None

	def rsets(self):
		for rec in self.__rset:
			self._fill(rec)
			yield self

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
		return self._name

	def get_pk_vec(self):
		return self._pk_vec

	def __build_ref_groups(self):
		self.__ref_group_vec = []
		self.__ref_group_map = {}
		for rel in self.__rel_vec:
			self.add_rel(rel)

	def add_rel(self, rel):
		new_ref_group = ref_group(rel)

		from sets import Set
		related = Set()
		for attr in rel.get_keys():
			if self.__ref_group_map.has_key(attr):
				related.add(self.__ref_group_map[attr])
			else:
				self.__ref_group_map[attr] = new_ref_group

		for group in related:
			for attr in group.get_keys()
				self.__ref_group_map[attr] = new_ref_group
			new_ref_group.join_group(group)

		# alternatively:
		#self.__ref_group_vec = list(Set(self.__ref_group_vec) - related)
		i = 0
		while i < len(self.__ref_group_vec):
			if self.__ref_group_vec[i] in related:
				self.__ref_group_vec.pop(i)
			else:
				i++

		self.__ref_group_vec.append(new_ref_group)

# alternative implementation (no keymap)
#		new_ref_group = ref_group(self, rel)
#
#		i = 0
#		while i < len(self.__ref_group_vec):
#			group_i = self.__ref_group_vec[i]
#
#			found = False
#			for key in rel.get_keys():
#				if group_i.has_key(key):
#					found = True
#					break
#
#			if found:
#				new_ref_group.join_group(group_i)
#				self.__ref_group_vec.pop(i)
#			else:
#				i++
#
#		self.__ref_group_vec.append(new_ref_group)

# alternative implementation (untested, probably fastest)
#		# An additional multi-key relation can introduce new interdependencies
#		# among groups so they have to be joined.
#		#
#		# For a single-key relation this algorithm will simply find the
#		# appropriate reference group to add the relation to or None, in which
#		# case a new reference group is constructed
#
#		first_group = None
#		i = 0
#		while i < len(self.__ref_group_vec):
#			group_i = self.__ref_group_vec[i]
#
#			found = False
#			for key in rel.get_keys():
#				if group_i.has_key(key):
#					found = True
#					break
#
#			if found:
#				if first_group is None
#					first_group = group_i
#					i++
#				else:
#					first_group.join(group_i)
#					self.__ref_group_vec.pop(i)
#			else:
#				i++
#
#		# Add the relation last to make sure that only keys are added that
#		# don't already exist in one of the reference groups.
#
#		if first_group is None:
#			# No existing dependencies. Construct a new reference group.
#			self.__ref_group_vec.append(ref_group(self, rel))
#		else:
#			# Add new reference group.
#			first_group.add_rel(rel)

# alternative implementation (works)
#		join = []
#
#		# find interdependent relations
#		for idx, ref_grp in enumerate(self.__ref_group_vec):
#			for key in rel.get_keys():
#				if ref_grp.has_key(key):
#					join.append(idx)
#					break
#
#		if len(join) > 0:
#			# join reference groups
#			ref_grp = self.__ref_group_vec[join[0]]
#
#			rev_range = range(len(join))
#			rev_range.reverse()
#			for i in rev_range:
#				ref_grp.join(self.__ref_group_vec.pop(join[i]))
#			ref_grp.add_rel(rel)
#		else:
#			# add new reference group
#			self.__ref_group_vec.append(ref_group(self, rel))

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
#		self.__ref_group_vec.append(ref_group(self, rel))

	def get_ref_group(self, attr):
		return self.__ref_group_map.get(attr, None)

	def attr_is_locked(self, attr):
		return self._attr_map[key].is_locked()

	def _require_pk_locks(self):
		found_missing = False

		for key in self._pk_vec:
			if not self.attr_is_locked(key):
				# TODO: is lock_map necessary? All keys have to be locked. The
				# user interace has to know which attribute belongs to which
				# reference group anyway (in order to display them in direct
				# succession so the user can choose which key to lock)
				#self.__lock_map[key] = None
				found_missing = True

		if found_missing:
			from error.missing_pk_lock import *
			raise missing_pk_lock()

	def accept(self, action):
		raise error(err_fail, errmsg.abstract_func)

	def has_attr(self, attr):
		# Do not raise an error if attribute does not exist. We
		# do not want the user to spy on secret attributes
		if not self._attr_map.has_key(attr):
			error(err_warn, errmsg.nonexisting_attr,
				'table: %s, attribute: %s' % (self._name, attr))

	def attr_accept(self, attr, action):
		if self.__has_attr(attr):
			self._attr_map[attr].accept(action)

	def attr_to_lock(self, attr):
		if self.__has_attr(attr):
			self._attr_map[attr].to_lock()

	def attr_lock(self, attr):
		if self.__has_attr(attr):
			self._attr_map[attr].lock()

	def get_attr_vec(self):
		return self._attr_vec

# TODO: remove
#	def get_attr(self, attr):
#		if not self._attr_map.has_key(attr):
#			raise error(err_fail, errmsg.nonexisting_attr,
#				'table: %s, attribute: %s' % (self._name, attr))
#
#		return self._attr_map[attr]

	def __get_attr_items(self):
		return self._attr_map.iteritems()

	def __get_attr_items_nopk(self):
		return [i for i in self._attr_map if i[0] not in self._pk_vec]

	def __get_attr_items_pk(self):
		return [(pk, self._attr_map[pk]) for pk in self._pk_vec]

	def get_attr_sql(self):
		return self.__sql_str(self.get_attr_items())

	def get_attr_sql_nopk(self):
		return self.__sql_str(self.get_attr_items_nopk())

	def get_attr_sql_pk(self):
		return self.__sql_str(self.get_attr_items_pk())

	def __sql_str(self, attr_items)
		sql_vec = ["%s='%s'" % (name, attr.sql_str())
			for (name, attr) in attr_items]

		return ", ".join(sql_vec)

	# fill in attribute values from given record
	def _fill(self, rec):

		# TODO: This also re-sets the primary keys. Make sure this does not
		# cause any problems
		for i, a in enumerate(self._attr_vec):
			attr = self._attr_map[a]
			if not attr.is_set():
				attr.set_sql(rset[i])

	# this has to be run after each configuration change
	def init(self):
		pass
