#
#  erm/helper.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

def sql_query(sql_str, session, glob):
	"""handle failures due to non-existent tables correctly"""

	from germ.lib.db_iface import db_iface
	from _mysql_exceptions import ProgrammingError

	done = False
	while not done:
		try:
			res = db_iface.query(sql_str)
		except ProgrammingError, e:
			table = db_iface.get_missing_table(e)

			if table is None:
				import sys
				exctype, exc, tb = sys.exc_info()
				raise exctype, exc, tb

			from helper import get_entity
			entity = get_entity(table, session, glob)
			entity.init()
			del entity
		else:
			done = True

	return res

# TODO: cache entities (immutable?)
def get_entity(ent_str, session, glob = globals()):
	try:
		mod = __import__('entity.' + ent_str, glob, locals(), [ent_str])
	except ImportError, e:
		from germ.error.error import error
		raise error(error.fail, "Could not find entity. " + \
				"ImportError: " + str(e), "entity: " + ent_str)

	entity_class = getattr(mod, ent_str)

	entity = entity_class()
	entity.set_session(session)

	return entity

# TODO: cache actions (immutable?)
def get_action(act_str, do_exec):
	action_class_str = 'act_' + act_str

	try:
		mod = __import__('germ.erm.' + action_class_str, globals(), locals(),
				[action_class_str])
	except ImportError, e:
		from germ.error.error import error
		raise error(error.fail, "Could not perform action. " + \
				"ImportError: " + str(e), "action: " + act_str)

	action_class = getattr(mod, action_class_str)

	return action_class(do_exec)

