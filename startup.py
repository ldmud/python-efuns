# This module can be used as a startup script.
#
# It will load all the other modules that offer the ldmud_efun entry point.
# In the configuration file ~/.ldmud-efuns single efuns can be deactivated
# with entries like this:
#
#   [efuns]
#   name_of_the_efun = off

from ldmudefuns.startup import startup

startup()
