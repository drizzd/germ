#
#  db_class_test.py: test the DB class
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from attr.attribute import *
from attr.date import date

from lib import misc
from ui_ht.attr_act_set import *
import datetime

#print misc.today()

attr = date('huhy', [ 'view'], None)
#attr.set_default()

attr.accept(attr_act_set(datetime.date(1975,1,1)))

print attr.get()

print attr.sql_str()
