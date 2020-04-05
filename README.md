# Python Efun package for LDMud

These are python efuns to be used with LDMud 3.5 and later.

This package contains the following efuns:
 * `strings` module:
    * `string wrap(string str [, int len [, int left]])`
    * `string wrap_say(string intro, string text [, int len [, int left]])`
    * `string left(string text, int len [,string pattern])`
 * `json` module:
    * `mixed json_parse(string jsonstring)`
    * `string json_serialize(mixed data)`
 * `reload` module:
    * `void python_reload()`
 * `help` module:
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
```

### Manually load the modules at startup

Add the following lines to your startup script:
```
import ldmudefuns.strings
import ldmudefuns.json
import ldmudefuns.reload

ldmudefuns.strings.register()
ldmudefuns.json.register()
ldmudefuns.reload.register()
ldmudefuns.help.register()
```

Have fun!
