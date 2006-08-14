#
#  cf.py: configuration
#
#  Copyright (C) 2005 Clemens Buchacher <drizzd@aon.at>
#

import os

### miscellaneous

buflen_max = 1024
log_file_path = '/var/log/lpms.log'
# de, en
lang = 'en'
admin_email = os.environ.get('SERVER_ADMIN')
# some more or less random string to identify password parameters
pwd_str = 'p294e5204'

### database

db_type = 'mysql'
db_host = 'my-mysql-server'
db_database = 'my-mysql-database'
db_user = 'my-mysql-user'
db_password = 'my-mysql-password'

### tournament planning

# require activation of team members
require_activation = False

### hypertext user interface

ht_root = os.environ.get('DOCUMENT_ROOT')
ht_index = os.environ.get('SCRIPT_NAME')
ht_docpath = '/home/myself/lpms/htdocs'
ht_default_page = None
ht_default_entity = None
ht_default_action = None
ht_parm_prefix_attr = 'a_'
ht_check_items = False
ht_tmp_path = '/tmp'
