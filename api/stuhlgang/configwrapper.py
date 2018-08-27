# vim: set expandtab ts=4 sw=4 filetype=python:

import importlib
import logging

import jinja2
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

        # Theoretically, a class-level decorator or metaclass applied to
        # the Relation classes could generate the factory for the class
        # and also add this stuff here.

        for database_table_name, module_path, factory_class_name in [

            ("people", "stuhlgang.pg.people", "PersonFactory"),
            ("webapp_sessions", "stuhlgang.pg.sessions", "SessionFactory"),
            ("patients", "stuhlgang.pg.stuhlgang", "PatientFactory"),
            ("patient_events", "stuhlgang.pg.stuhlgang", "PatientEventFactory"),
            ("patient_caretakers", None, None),
            ("provider_patient_links", None, None),

        ]:

            if module_path and factory_class_name:

                module = importlib.import_module(module_path)
                factory_class = getattr(module, factory_class_name)

                psycopg2.extras.register_composite(
                    database_table_name,
                    pgconn,
                    factory=factory_class)

            else:

                psycopg2.extras.register_composite(
                    database_table_name,
                    pgconn)

        log.info('Just registered composite types in psycopg2')

        return pgconn


    def add_more_stuff_to_jinja2_globals(self):

        j = self.get_jinja2_environment()

        j.add_extension('jinja2.ext.do')

        j.loader.mapping['emailtemplates'] = jinja2.PackageLoader(
            'stuhlgang',
            'emailtemplates')

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
