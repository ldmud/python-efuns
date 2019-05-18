# This module can be used as a startup script.
#
# It will load all the other modules that offer the ldmud_efun entry point.
# In the configuration file ~/.ldmud-efuns single efuns can be deactivated
# with entries like this:
#
#   [efuns]
#   name_of_the_efun = off

def startup():
    import pkg_resources, traceback, sys, os, configparser
    import ldmud

    config = configparser.ConfigParser()
    config['efuns'] = {}
    config.read(os.path.expanduser('~/.ldmud-efuns'))
    efunconfig = config['efuns']

    for entry_point in pkg_resources.iter_entry_points('ldmud_efun'):
        if efunconfig.getboolean(entry_point.name, True):
            try:
                print("Registering Python efun", entry_point.name)
                ldmud.register_efun(entry_point.name, entry_point.load())
            except:
                traceback.print_exc()

startup()
