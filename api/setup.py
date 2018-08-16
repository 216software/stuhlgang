# vim: set expandtab ts=4 sw=4 filetype=python fileencoding=utf8:

from setuptools import find_packages, setup

setup(

    name="stuhlgang",

    version="0.0.1",

    packages=find_packages(),

    include_package_data=True,

    package_dir={"stuhlgang": "stuhlgang"},

    scripts=[
        "stuhlgang/scripts/stuhlgang-run-webapp",
        "stuhlgang/scripts/stuhlgang-upgrade-database",
        "stuhlgang/scripts/stuhlgang-rebuild-database",
        "stuhlgang/scripts/stuhlgang-config",
        "stuhlgang/scripts/stuhlgang-yaml-example",
    ],

)
