import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ldmud-efuns",
    version="0.0.1",
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
        'ldmud_efuns': [
              'strings = ldmudefuns.strings:register',
              'json    = ldmudefuns.json:register',
              'reload  = ldmudefuns.reload:register',
        ]
    },
    zip_safe=False,
)
