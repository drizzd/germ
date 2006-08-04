#
#  erm/entity.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from germ.txt import errmsg

from ref_group import *

class entity:
	def __init__(self, attributes, primary_keys, relations, condition,
			item_txt, action_txt, action_report, perm, pre, post, magic_var):
		self._name = self.__class__.__name__

		self.__item_txt = item_txt
		self.__action_txt = action_txt
		self.__action_report = action_report

		self._attr_map = dict(attributes)
		self._attr_ids = []
		for a in attributes:
			self._attr_ids.append(a[0])

		self._rset = None

		from sets import Set
		self._pk_set = Set(primary_keys)
		self.__rel_vec = relations
		self.__condition = condition
		self.__lock_map = {}

		self.__perm = perm
		self.__pre = pre
		self.__post = post

		self.__magic_var = magic_var

		self._session = None
		self._globals = None

	# this has to be called immediately after instantiation
	def init(self, session, globals):
		self._session = session
		self._globals = globals

		self.__build_ref_groups()

	def get_globals(self):
		return self._globals

	def magic_var(self, var):
		magic_func = self.__magic_var.get(var)
		
		from germ.lib.misc import call_if

		return call_if(magic_func)

	def get_var(self, var):
		return self._session.get(var)

	def item_txt(self, act_str):
		text = self.__item_txt.get(act_str, self.action_txt(act_str))

		return text

	def action_txt(self, act_str):
		from germ.txt import misc
		text = self.__action_txt.get(act_str, misc.action.get(act_str))

		if text is None:
			from germ.error.error import error
			raise error(error.warn, 'No action description', 'action: %s' % \
					act_str)
		
		return text

	def action_report(self, act_str):
		report = self.__action_report.get(act_str)

		if report is None:
			report = { 'en': '' }

		return report
		
	def get_condition(self, act_str):
		from germ.lib import misc

		return misc.get_cond(self.__condition, act_str)

	def get_session(self):
		return self._session

	def set_rset(self, rset):
		if self._rset is not None:
			pass
			#from germ.error.error import error
			#raise error(error.fail, "Attempt to set result set twice",
			#	"entity: %s" % self._name)

		self._rset = rset

	def has_rset(self):
		return self._rset is not None

	def rsets(self, act_str):
		for rec in self._rset:
			self._fill(rec, act_str, overwrite = True)
			yield self

	def pre(self, act_str):
		from germ.lib.misc import do_nothing

		return self.__pre.get(act_str, do_nothing)()

	def post(self, act_str):
		from germ.lib.misc import do_nothing

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
		# An additional multi-key relation can introduce new interdependencies
		# among groups so they have to be joined.
		#
		# For a single-key relation this algorithm will simply find the
		# appropriate reference group to add the relation to or None, in which
		# case a new reference group is constructed

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

	def pks_locked(self):
		for key in self._pk_set:
			if not self._attr_map[key].is_locked():
				return False

		return True

	def accept(self, action):
		from germ.lib.misc import call_if

		# The tests are evaluated in the following order. If any of the tests
		# is not specified, proceed to the next item.
		#
		# 1. 'none':	If this fails, deny permission, otherwise proceed.
		# 2. act_str:	This either denies or grants permission. Only proceed
		# 				to the next test if act_str specification does not
		# 				exist.
		# 3. 'all':		If this fails, deny permission
		# 4. grant permission
		#
		if not (call_if(self.__perm.get('none', True)) and \
				call_if(self.__perm.get(str(action),
				call_if(self.__perm.get('all', True))))):
			from germ.error.perm_denied import perm_denied
			raise perm_denied()

		self.do_accept(action)

	def do_accept(self, action):
		raise error(error.fail, errmsg.abstract_func)

	def __has_attr(self, attr):
		has_attr = self._attr_map.has_key(attr)

		## Do not raise an error if attribute does not exist. We
		## do not want the user to spy on secret attributes
		#if not has_attr:
		#	from germ.error.error import error
		#	error(error.warn, errmsg.nonexistent_attr,
		#		'table: %s, attribute: %s' % (self._name, attr))

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

			from germ.error.error import error
			error(error.debug, 'checking attribute', aid)

			if attr.dyn_perm(action):
				yield attr
			else:
				from germ.attr.dummy import dummy
				yield dummy()

	def get_attr_vec(self, action):
		return [attr for attr in self._attr_ids \
				if self._attr_map[attr].dyn_perm(action)]
		#return [attr for attr in self._attr_ids \
		#		if attr in self._pk_set or \
		#		self._attr_map[attr].dyn_perm(action)]

	def set_default(self):
		from germ.error.invalid_parm import invalid_parm
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

			if attr in self._pk_set or a.dyn_perm(action):
				return a

		#from germ.error.error import error
		#raise error(error.fail, errmsg.nonexistent_attr,
		#	'table: %s, attribute: %s' % (self._name, attr))

		from germ.attr.dummy import dummy
		return dummy()

	def __get_attr_items(self):
		return self._attr_map.iteritems()
		#return [i for i in self._attr_map.iteritems() \
		#		if i[1].is_set()]

	def __get_attr_items_nopk(self):
		return [i for i in self._attr_map.iteritems() \
				if i[0] not in self._pk_set and i[1].is_set()]

	def __get_attr_items_pk(self):
		return [(pk, self._attr_map[pk]) for pk in self._pk_set]

	def __get_attr_items_pk_alias(self, alias):
		return [('%s.%s' % (alias, pk), self._attr_map[pk])
				for pk in self._pk_set]

	def get_attr_sql(self):
		return self.__sql_str(self.__get_attr_items())

	def get_attr_sql_nopk(self):
		return self.__sql_str(self.__get_attr_items_nopk())

	def get_attr_sql_pk(self):
		return self.__sql_str(self.__get_attr_items_pk(), ' AND ')

	def get_attr_sql_pk_alias(self, alias):
		return self.__sql_str(self.__get_attr_items_pk_alias(alias), ' AND ')

	def __sql_str(self, attr_items, delim = ', '):
		sql_vec = ["%s = '%s'" % (name, attr.sql_str())
			for (name, attr) in attr_items]

		return delim.join(sql_vec)

	# fill in attribute values from given record
	def _fill(self, rec, act_str, overwrite = False):
		#rec = self._rset[0]

		for i, aid in enumerate(self._attr_ids):
			attr = self._attr_map[aid]

			if attr.dyn_perm(act_str):
				#if not attr.is_set():
				#	attr.set_sql(rec[i])
				if overwrite or not attr.is_set():
					attr.set_sql(rec[i])
				else:
					from germ.error.error import error
					error(error.debug, 'not writing set attribute (%s)' \
							% aid)
			elif not aid in self._pk_set:
				if attr.is_set():
					from germ.error.error import error
					error(error.debug, 'overwriting attribute (%s)' % aid)

				attr.set_sql(rec[i])
			else:
				from germ.error.error import error
				error(error.debug, 'not setting attribute (%s)' % aid)

#			if not (attr.is_set() and attr.dyn_perm(act_str)(attr)):
#				attr.set_sql(rec[i])

	def substitute_attr(self, key, attr):
		self._attr_map[key] = attr
