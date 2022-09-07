import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ldmud-efuns",
    version="0.2.2",
    author="LDMud Team",
    author_email="ldmud-dev@UNItopia.DE",
    description="Python Efun management package for LDMud",
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
              'python_reload    = ldmudefuns.reload:reload_modules',
              'python_efun_help = ldmudefuns.help:python_efun_help',
        ]
    },
    zip_safe=False,
)
