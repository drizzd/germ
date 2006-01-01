#!/usr/bin/python

import sys
# path to pso and germ (if not already in default search path)
sys.path.append("/home/myself/py")
# path to the actual application (germ looks for entity specifications in 'entity')
sys.path.append("/home/myself/lpms")

from germ.ui_ht.handler import handler

from pso.service import ServiceHandler
ServiceHandler().run(handler)
