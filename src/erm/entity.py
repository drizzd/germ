#
#  entity.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from txt import errmsg

from ref_group import *

class entity:
	def __init__(self, attributes, primary_keys, relations, condition,
			item_txt, action_txt, action_report, perm, pre, post):
		self._name = self.__class__.__name__

		self.__item_txt = item_txt
		self.__action_txt = action_txt
		self.__action_report = action_report

		self._attr_map = dict(attributes)
		self._attr_ids = []
		for a in attributes:
			self._attr_ids.append(a[0])

		self.__rset = None

		from sets import Set
		self._pk_set = Set(primary_keys)
		self.__rel_vec = relations
		self.__condition = condition
		self.__lock_map = {}

		self.__perm = perm
		self.__pre = pre
		self.__post = post

		self._session = None
		self.__build_ref_groups()

		self.init()

	def get_var(self, var):
		return self._session.get(var)

	def item_txt(self, act_str):
		text = self.__item_txt.get(act_str, self.__action_txt.get(act_str))

		if text is None:
			from error.error import error
			raise error(error.warn, 'No item description', 'action: %s' % \
					act_str)

		return text

	def action_txt(self, act_str):
		from txt import misc
		text = self.__action_txt.get(act_str, misc.action.get(act_str))

		if text is None:
			from error.error import error
			raise error(error.warn, 'No action description', 'action: %s' % \
					act_str)
		
		return text

	def action_report(self, act_str):
		report = self.__action_report.get(act_str)

		if report is None:
			report = { 'en': '' }

		return report
		
	def set_session(self, session):
		self._session = session
	
	def get_condition(self):
		return self.__condition

	def get_session(self):
		return self._session

	def set_rset(self, rset):
		if self.__rset is not None:
			from error.error import error
			raise error(error.fail, "Attempt to set result set twice",
				"entity: %s" % self._name)

		self.__rset = rset

	def has_rset(self):
		return self.__rset is not None

	def rsets(self):
		for rec in self.__rset:
			self._fill(rec)
			yield self

	def pre(self, act_str):
		from lib.misc import do_nothing

		return self.__pre.get(act_str, do_nothing)()

	def post(self, act_str):
		from lib.misc import do_nothing

		return self.__post.get(act_str, do_nothing)()

	def get_name(self):
		return self._name

	def get_pk_set(self):
		return self._pk_set

	def __build_ref_groups(self):
		self.__ref_group_vec = []
		self.__ref_group_map = {}
		for rel in self.__rel_vec:
			self.add_rel(rel)

	def get_ref_group_vec(self):
		return self.__ref_group_vec

	def add_rel(self, rel):
		new_ref_group = ref_group(rel, self)

		from sets import Set
		related = Set()
		for attr in rel.get_keys():
			if self.__ref_group_map.has_key(attr):
				related.add(self.__ref_group_map[attr])
			else:
				self.__ref_group_map[attr] = new_ref_group

		for group in related:
			for attr in group.get_rel_keys():
				self.__ref_group_map[attr] = new_ref_group
			new_ref_group.join_group(group)

		# alternatively:
		#self.__ref_group_vec = list(Set(self.__ref_group_vec) - related)
		i = 0
		while i < len(self.__ref_group_vec):
			if self.__ref_group_vec[i] in related:
				self.__ref_group_vec.pop(i)
			else:
				i += 1

		self.__ref_group_vec.append(new_ref_group)

# alternative implementation (no keymap)
#		new_ref_group = ref_group(rel, self)
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
#				i += 1
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
#				if first_group is None:
#					first_group = group_i
#					i += 1
#				else:
#					first_group.join(group_i)
#					self.__ref_group_vec.pop(i)
#			else:
#				i += 1
#
#		# Add the relation last to make sure that only keys are added that
#		# don't already exist in one of the reference groups.
#
#		if first_group is None:
#			# No existing dependencies. Construct a new reference group.
#			self.__ref_group_vec.append(ref_group(rel, self))
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
#			self.__ref_group_vec.append(ref_group(rel, self))

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
#			if ref_grp_join is not None:
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
#		self.__ref_group_vec.append(ref_group(rel, self))

	def get_ref_group(self, attr):
		return self.__ref_group_map.get(attr, None)

	def _require_pk_locks(self):
		found_missing = False

		for key in self._pk_set:
			if not self._attr_map[key].is_locked():
				# TODO: is lock_map necessary? All keys have to be locked. The
				# user interace has to know which attribute belongs to which
				# reference group anyway (in order to display them in direct
				# succession so the user can choose which key to lock)
				#self.__lock_map[key] = None
				found_missing = True

		if found_missing:
			from error.missing_pk_lock import missing_pk_lock
			raise missing_pk_lock()

	def accept(self, action):
		from lib.misc import always_true

		from error.error import error
		error(error.debug, 'checking permission', 'entity: %s, action: %s' % \
				(self._name, str(action)))

		if isinstance(self.__perm, dict):
			perm = self.__perm.get(str(action), always_true)()
		else:
			perm = self.__perm()

		if not perm:
			from error.perm_denied import perm_denied
			raise perm_denied()

		self.do_accept(action)

	def do_accept(self, action):
		raise error(error.fail, errmsg.abstract_func)

	def __has_attr(self, attr):
		has_attr = self._attr_map.has_key(attr)

		# Do not raise an error if attribute does not exist. We
		# do not want the user to spy on secret attributes
		if not has_attr:
			from error.error import error
			error(error.warn, errmsg.nonexistent_attr,
				'table: %s, attribute: %s' % (self._name, attr))

		return has_attr

	def get_attr_ids(self):
		return self._attr_ids

	def attr_id_iter(self, action):
		for id in self._attr_ids:
			if self._attr_map[id].perm(action):
				yield id

	def attr_iter(self, action):
		for aid in self._attr_ids:
			attr = self._attr_map[aid]
			if attr.perm(action):
				yield attr

	def get_attr_vec(self, action):
		return [attr for attr in self._attr_ids \
				if attr in self._pk_set or self._attr_map[attr].perm(action)]

	def set_default(self):
		from error.invalid_parm import invalid_parm
		found_invalid_parm = False

		for attr in self._attr_map.itervalues():
			if not attr.is_set():
				try:
					attr.set_default()
				except invalid_parm:
					found_invalid_parm = True

		if found_invalid_parm:
			raise invalid_parm()

	def get_attr_nocheck(self, attr):
		return self._attr_map[attr]

	def get_attr(self, attr, action):
		if self.__has_attr(attr):
			a = self._attr_map[attr]

			if attr in self._pk_set or a.perm(action):
				return a

		from error.error import error
		raise error(error.fail, errmsg.nonexistent_attr,
			'table: %s, attribute: %s' % (self._name, attr))

	def __get_attr_items(self):
		return self._attr_map.iteritems()

	def __get_attr_items_nopk(self):
		return [i for i in self._attr_map.iteritems() if i[0] not in self._pk_set]

	def __get_attr_items_pk(self):
		return [(pk, self._attr_map[pk]) for pk in self._pk_set]

	def get_attr_sql(self):
		return self.__sql_str(self.__get_attr_items())

	def get_attr_sql_nopk(self):
		return self.__sql_str(self.__get_attr_items_nopk())

	def get_attr_sql_pk(self):
		return self.__sql_str(self.__get_attr_items_pk(), ' AND ')

	def __sql_str(self, attr_items, delim = ', '):
		sql_vec = ["%s = '%s'" % (name, attr.sql_str())
			for (name, attr) in attr_items]

		return delim.join(sql_vec)

	# fill in attribute values from given record
	def _fill(self, rec):
		for i, aid in enumerate(self._attr_ids):
			attr = self._attr_map[aid]

			if not attr.is_set():
				attr.set_sql(rec[i])

	# this has to be invoked after each configuration change
	def init(self):
		pass
