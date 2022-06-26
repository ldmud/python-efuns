def startup():
    """ Loads all registered packages that offer the ldmud_efun entry point.

    In the configuration file ~/.ldmud-efuns single efuns can be deactivated
    with entries like:

        [efuns]
        name_of_the_efun = off
    """

    import pkg_resources, traceback, sys, os, configparser
    import ldmud

    config = configparser.ConfigParser()
    config['efuns'] = {}
    config['types'] = {}
    config.read(os.path.expanduser('~/.ldmud-efuns'))

    ep_types = []
    if hasattr(ldmud, 'register_type'):
        ep_types.append(('ldmud_type', 'type', config['types'], ldmud.register_type,))
    if hasattr(ldmud, 'register_efun'):
        ep_types.append(('ldmud_efun', 'efun', config['efuns'], ldmud.register_efun,))

    for ep_name, ep_desc, ep_config, ep_register in ep_types:
        for entry_point in pkg_resources.iter_entry_points(ep_name):
            if ep_config.getboolean(entry_point.name, True):
                try:
                    print("Registering Python", ep_desc, entry_point.name)
                    ep_register(entry_point.name, entry_point.load())
                except:
                    traceback.print_exc()
