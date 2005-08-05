#
#  pk_submit_relation.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from relation import *

# This class is currently unused for the reason described below
class pk_submit_relation(relation):
	def __init__(
			self, table, keys,
			alias = None, cond = None, outer_join = None):
		relation.__init__(self, table, keys, alias, cond, outer_join)

	# This is really cool. But not always.
	#
	# This handles the case of a primary key that is not a foreign key at the
	# same time. This means that we would have to lock the value to give an
	# appropriate list of allowed keys for the other relations from the same
	# reference group. The question is whether this behaviour is really
	# desirable. Consider the following two cases:
	#
	# First, we have a 'team' table. It has the keys 'name' and 'tournament'.
	# To give an accurate list of available tournaments we would first have to
	# give the team name, because then we know which tournaments already have a
	# team with that name and are therefore not available. On the other hand,
	# if a user wants to form a team and he can chose a name for his team that
	# already exists in the desired tournamente he can probably easily think of
	# a different name.
	#
	# If we had specified the team name first the desired tournament would not
	# have been an available option, which is not a very user-friendly
	# behaviour.
	#
	# Second, consider a 'game' table, which contains all the games for a
	# tournament. It has the keys 'round', 'team1' and 'team2' (and
	# 'tournament' of course, but that's irrelevant for our discussion). To
	# give an accurate list of available team combinations we would first have
	# to specify the 'round' for which we want to add a new game. This is
	# great. Usually we know exactly which round we currently have and the
	# system will provide the teams that are still available for this round.
	#
	# If, on the other hand, we specify the round last we might end up trying
	# all possible combinations of teams until we finally find the right one
	# for the desired round. Of course, we could always look at the game
	# listing and find out which teams are not assigned to a game yet. But
	# that's not particularly user friendly.
	#
	# Thus, the best solution depends on the situation. So, we let the user
	# decide which key to lock first. (To be implemented in user interface)
	#
	# Also, this problem doesn't only exist for primary keys. It applies to any
	# kind of attribute that's not a foreign key (i.e. for which there is no
	# list of available items to choose from) but that has to meet some kind of
	# condition, like uniquess.
	def handle_unknown_key(self, key, attr_map, join_cond):
		# Here we check if the key is locked. It is a primary key, and it is
		# not a relation because if it was, this function would never be
		# called. We always add the primary key relation to the reference
		# groups last. Thus all other relations will be evaluated first and the
		# key would already point to another relation, if another relation
		# for this key existed.

		attr = attr_map[key]

		if attr.is_locked():
			# exclude all matches for this key (this condition is used in a
			# LEFT JOIN ... WHERE pk0 IS NULL)
			join_cond.append("\n\t\t%s = '%s'" %
				(self.get_colref(key), attr.sql_str()))

		# Indicate that this is not a foreign key
		return None
