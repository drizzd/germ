#
#  cf.py: configuration
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

db_type = 'mysql'
db_host = 'localhost'
db_database = 'tilt_new'
db_user = 'tilt'
db_password = 'gfx17'

buflen_max = 1024
log_file_path = '/var/log/germ.log'
# de, en
lang = 'en'
admin_name = 'Clemens Buchacher'
admin_email = 'drizzd@aon.at'

ht_root = '/var/www'
ht_path = 'lpms'
ht_index = 'ui_ht/handler.py'
ht_docpath = 'htdocs'
ht_default_entity = 'users'
ht_default_action = 'submit'
