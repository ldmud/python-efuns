import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ldmud-efuns",
    version="0.0.5",
    author="LDMud Team",
    author_email="ldmud-dev@UNItopia.DE",
    description="Python Efun package for LDMud",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ldmud/python-efuns",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'ldmud_efun': [
              'wrap             = ldmudefuns.strings:efun_wrap',
              'wrap_say         = ldmudefuns.strings:efun_wrap_say',
              'left             = ldmudefuns.strings:efun_left',
              'json_serialize   = ldmudefuns.json:efun_json_serialize',
              'json_parse       = ldmudefuns.json:efun_json_parse',
              'python_reload    = ldmudefuns.reload:reload_modules',
              'python_efun_help = ldmudefuns.help:python_efun_help',
        ]
    },
    zip_safe=False,
)
