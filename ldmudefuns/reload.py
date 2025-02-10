import importlib, sys
import ldmud

from .internal import get_registration_types, get_entry_points, metadata

def reload_modules():
    """
    SYNOPSIS
            void python_reload()

    DESCRIPTION
            Reloads all Python efuns. All packages providing the "ldmud_efuns"
            entry point are loaded. If they were already loaded, they are reloaded.
            Then the entry point is executed to register the efuns.

            Before reloading the function on_reload() is called in the module.

    SEE ALSO
            python_efun_help(E)
    """
    importlib.reload(metadata)
    modules = dict(sys.modules)
    reloaded = set()
    ep_types = get_registration_types()

    for ep_name, ep_desc, ep_config, ep_register in ep_types:
        for entry_point in get_entry_points(ep_name):
            if ep_config.getboolean(entry_point.name, True):
                # Remove the corresponding modules from sys.modules
                # so they will be reloaded.
                names = entry_point.module.split('.')
                for module in ('.'.join(names[:pos]) for pos in range(len(names), 0, -1)):
                    if not module in modules or module in reloaded:
                        break

                    try:
                        sys.modules[module].on_reload()
                    except:
                        pass

                    del sys.modules[module]
                    reloaded.add(module)
                    print("Reload module", module)

    for ep_name, ep_desc, ep_config, ep_register in ep_types:
        for entry_point in get_entry_points(ep_name):
            if ep_config.getboolean(entry_point.name, True):
                try:
                    print("Re-registering Python", ep_desc, entry_point.name)
                    ep_register(entry_point.name, entry_point.load())
                except:
                    traceback.print_exc()

def register():
    ldmud.register_efun("python_reload", reload_modules)
