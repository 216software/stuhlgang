# vim: set expandtab ts=4 sw=4 filetype=python:

import logging

import psycopg2.extras

from horsemeat import configwrapper

log = logging.getLogger(__name__)

class ConfigWrapper(configwrapper.ConfigWrapper):

    # Where are the config files?
    configmodule = "stuhlgang.yamlfiles"

    @property
    def dispatcher_class(self):

        from stuhlgang.webapp.framework.dispatcher import Dispatcher
        return Dispatcher

    def register_composite_types(self, pgconn):

        from stuhlgang.pg.people import PersonFactory

        psycopg2.extras.register_composite('people', pgconn,
          factory=PersonFactory)

        from stuhlgang.pg.sessions import SessionFactory

        psycopg2.extras.register_composite('webapp_sessions', pgconn,
          factory=SessionFactory)

        log.info('Just registered composite types in psycopg2')

        return pgconn


    def add_more_stuff_to_jinja2_globals(self):

        j = self.get_jinja2_environment()

        j.add_extension('jinja2.ext.do')

    @classmethod
    def print_example_yaml(cls):

        import pkg_resources

        print(pkg_resources.resource_string(
            "stuhlgang",
            "yamlfiles/prod.yaml.example"))

if __name__ == "__main__":

    import argparse
    ap = argparse.ArgumentParser(
        description="Print a value from the config file")

    ap.add_argument("yaml_file_name")
    ap.add_argument("property")

    args = ap.parse_args()

    cw = ConfigWrapper.from_yaml_file_name(args.yaml_file_name)

    print(getattr(cw, args.property))
