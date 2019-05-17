import importlib, pkg_resources, site, sys
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
    """
    importlib.reload(site)
    ws = pkg_resources.WorkingSet()
    modules = dict(sys.modules)

    for entry_point in ws.iter_entry_points('ldmud_efuns'):
        fun = entry_point.load()
        if fun.__module__ in modules:
            modob = modules[fun.__module__]
            try:
                modob.on_reload()
            except:
                pass
            importlib.reload(modob)
        fun()

def register():
    ldmud.register_efun("python_reload", reload_modules)
