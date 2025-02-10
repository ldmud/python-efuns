from .internal import get_registration_types, get_entry_points

def startup():
    """ Loads all registered packages that offer the ldmud_efun entry point.

    In the configuration file ~/.ldmud-efuns single efuns can be deactivated
    with entries like:

        [efuns]
        name_of_the_efun = off
    """

    import traceback

    for ep_name, ep_desc, ep_config, ep_register in get_registration_types():
        for entry_point in get_entry_points(ep_name):
            if ep_config.getboolean(entry_point.name, True):
                try:
                    print("Registering Python", ep_desc, entry_point.name)
                    ep_register(entry_point.name, entry_point.load())
                except:
                    traceback.print_exc()
