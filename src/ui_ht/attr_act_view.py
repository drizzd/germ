#
#  attr_act_view.py
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

from attr_act_form import *

class attr_act_view:
	def __init__(self, htmltext):
		self.__htmltext = htmltext

	def visit_string(attr):
		self.__htmltext += attr.sql_str()

	def visit_int(attr):
		self.__htmltext += attr.sql_str()

	def visit_date(attr):
		date = attr.get()
		self.__htmltext += date.strftime("%Y-%m-%d")

	def visit_bool(attr):
		self.__htmltext += '<INPUT type="checkbox"%s disabled>' % \
				attr.get() and ' checked' or ''
