import importlib, pkg_resources, site, sys, os, configparser
import ldmud

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
    importlib.reload(site)
    ws = pkg_resources.WorkingSet()
    modules = dict(sys.modules)
    reloaded = set()

    config = configparser.ConfigParser()
    config['efuns'] = {}
    config.read(os.path.expanduser('~/.ldmud-efuns'))
    efunconfig = config['efuns']

    for entry_point in ws.iter_entry_points('ldmud_efun'):
        if efunconfig.getboolean(entry_point.name, True):
            # Remove the corresponding modules from sys.modules
            # so they will be reloaded.
            names = entry_point.module_name.split('.')
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

            ldmud.register_efun(entry_point.name, entry_point.load())

def register():
    ldmud.register_efun("python_reload", reload_modules)
