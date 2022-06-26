# Python Efun package for LDMud

These are routines and python efuns for management of Python efuns and types with LDMud 3.5 and later.

The package allows efuns and types to be dynamically detected, registered and reloaded.

This package contains the following efuns:
 * `void python_reload()`
 * `string python_efun_help(string efunname)`

## Usage

### Install from the python package index

The efun package can be downloaded from the python package index:

```
pip3 install --user ldmud-efuns
```

### Build & install the package yourself

You can build the package yourself.

First clone the repository
```
git clone https://github.com/ldmud/python-efuns.git
```

Install the package
```
cd python-efuns
python3 setup.py install --user
```

### Automatically load the modules at startup

Use [startup.py](https://github.com/ldmud/python-efuns/blob/master/startup.py) as the Python startup script for LDMud.
It will automatically detect the installed python efuns and load them.

You can deactivate single efuns with a configfile `.ldmud-efuns`
in your home directory, with the following contents
```
[efuns]
name_of_the_efun = off

[types]
name_of_the_type = off
```

### Manually load the modules at startup

Add the following lines to your startup script:
```
import ldmudefuns.reload
import ldmudefuns.help

ldmudefuns.reload.register()
ldmudefuns.help.register()
```

Have fun!
