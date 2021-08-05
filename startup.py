# This module can be used as a startup script.
#
# It will load all the other modules that offer the ldmud_efun entry point.
# In the configuration file ~/.ldmud-efuns single efuns can be deactivated
# with entries like this:
#
#   [efuns]
#   name_of_the_efun = off
# 
# If you would like to load configuration from a different file, pass the
# path to the startup function, e.g. startup(config_path='~/.ldmud-efuns-test')

from ldmudefuns.startup import startup

startup()
