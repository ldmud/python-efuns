import os
import configparser
import ldmud

try:
    import importlib.metadata as metadata
except ModuleNotFoundError:
    import importlib_metadata as metadata

def get_config():
    config = configparser.ConfigParser()
    config['efuns'] = {}
    config['types'] = {}
    config.read(os.path.expanduser('~/.ldmud-efuns'))
    return config

def get_registration_types():
    ep_types = []
    config = get_config()
    if hasattr(ldmud, 'register_type'):
        ep_types.append(('ldmud_type', 'type', config['types'], ldmud.register_type))
    if hasattr(ldmud, 'register_efun'):
        ep_types.append(('ldmud_efun', 'efun', config['efuns'], ldmud.register_efun))
    return ep_types

def get_entry_points(group_name):
    eps = metadata.entry_points()

    # Prior to importlib_metadata 5.0 and Python 3.12 entry_points()
    # returned a dictionary of entry points keyed to group.
    if isinstance(eps, dict):
        return eps.get(group_name, ())

    # For modern versions of importlib_metadata and Python 3.12
    # entry_points() returns an EntryPoints object that can be
    # queried with select().
    return eps.select(group=group_name)
