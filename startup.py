# This module can be used as a startup script.
#
# It will load all the other modules that offer
# the ldmud_efuns entry point.

import pkg_resources, traceback
import ldmud

for entry_point in pkg_resources.iter_entry_points('ldmud_efuns'):
    try:
        entry_point.load()()
    except:
        traceback.print_exc()
