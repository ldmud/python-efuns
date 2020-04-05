import pkg_resources, os, configparser
import ldmud

def python_efun_help(efunname: str) -> str:
    """
    SYNOPSIS
            string python_efun_help(string efunname)

    DESCRIPTION
            Returns the docstring for the given Python efun, if there is any.

    SEE ALSO
            python_reload(E)
    """
    config = configparser.ConfigParser()
    config['efuns'] = {}
    config.read(os.path.expanduser('~/.ldmud-efuns'))
    efunconfig = config['efuns']

    if not efunconfig.getboolean(efunname, True):
        return None

    ws = pkg_resources.WorkingSet()
    for entry_point in ws.iter_entry_points('ldmud_efun', efunname):
        doc = getattr(entry_point.load(), '__doc__', None)
        if doc:
            # Trim algorithm from PEP 257
            lines = doc.expandtabs().splitlines()
            indent = len(doc)

            #Determine indentation
            for line in lines[1:]:
                stripped = line.lstrip()
                if stripped:
                    indent = min(indent, len(line) - len(stripped))

            # Remove indentation
            trimmed = [lines[0].strip()]
            if indent < len(doc):
                for line in lines[1:]:
                    trimmed.append(line[indent:].rstrip())

            # Strip off trailing and leading blank lines:
            while trimmed and not trimmed[-1]:
                trimmed.pop()
            while trimmed and not trimmed[0]:
                trimmed.pop(0)

            # Return a single string:
            return '\n'.join(trimmed) + '\n'

def register():
    ldmud.register_efun("python_efun_help", python_efun_help)
