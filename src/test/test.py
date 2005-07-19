#
#  db_class_test.py: test the DB class
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
# 

print "-> Importing modules ..."

from erm.act_submit import *
from erm.ent_table import *
from erm.tbl_act_view import *

entity = 'team_members'
__import__('entity.%s' % entity, globals(), locals(), [])

print "-> Instantiating entity ..."

t1 = team_members()

print "-> Setting attributes ..."

t1._entity__attr_map['party'].set('tilt7')
t1._entity__attr_map['party'].lock()

print "-> Instantiating action ..."

a1 = act_submit('submit')

print "-> Executing action ..."

t1.accept(a1)

print "-> All done."
