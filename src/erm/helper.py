#
#  helper.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

def get_entity(ent_str, session, glob = globals()):
	try:
		mod = __import__('entity.' + ent_str, glob, locals(), [ent_str])
	except ImportError, e:
		from error import *
		raise error(err_fail, "Could not find entity. " + \
				"ImportError: " + str(e), "entity: " + ent_str)

	entity_class = getattr(mod, ent_str)

	entity = entity_class()
	entity.set_session(session)

	return entity

def get_action(act_str, do_exec):
	action_class_str = 'act_' + act_str

	try:
		mod = __import__('erm.' + action_class_str, globals(), locals(),
				[action_class_str])
	except ImportError, e:
		from error import *
		raise error(err_fail, "Could not perform action. " + \
				"ImportError: " + str(e), "action: " + act_str)

	action_class = getattr(mod, action_class_str)

	return action_class(do_exec)

