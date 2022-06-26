def startup():
    """ Loads all registered packages that offer the ldmud_efun entry point.

    In the configuration file ~/.ldmud-efuns single efuns can be deactivated
    with entries like:

        [efuns]
        name_of_the_efun = off
    """

    import traceback, sys, os, configparser
    import ldmud

    try:
        import importlib.metadata as metadata
    except ModuleNotFoundError:
        import importlib_metadata as metadata

    config = configparser.ConfigParser()
    config['efuns'] = {}
    config['types'] = {}
    config.read(os.path.expanduser('~/.ldmud-efuns'))

    ep_types = []
    if hasattr(ldmud, 'register_type'):
        ep_types.append(('ldmud_type', 'type', config['types'], ldmud.register_type,))
    if hasattr(ldmud, 'register_efun'):
        ep_types.append(('ldmud_efun', 'efun', config['efuns'], ldmud.register_efun,))

    eps = metadata.entry_points()

    for ep_name, ep_desc, ep_config, ep_register in ep_types:
        for entry_point in eps.get(ep_name,()):
            if ep_config.getboolean(entry_point.name, True):
                try:
                    print("Registering Python", ep_desc, entry_point.name)
                    ep_register(entry_point.name, entry_point.load())
                except:
                    traceback.print_exc()
