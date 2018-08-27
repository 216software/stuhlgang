# vim: set expandtab ts=4 sw=4 filetype=python fileencoding=utf8:

import unittest

from stuhlgang import configwrapper
from stuhlgang import pg

class Test1(unittest.TestCase):

    def setUp(self):

        # TODO: make a test yaml
        self.cw = configwrapper.ConfigWrapper.from_yaml_file_name("xps.yaml")
        self.cw.set_as_default()

        self.matt = pg.people.Person.by_email_address(
            self.cw.get_pgconn(),
            "matt@216software.com")

    def tearDown(self):

        self.cw.get_pgconn().rollback()

    def test_add_patients(self):

        charlie = pg.Patient.insert(
            self.cw.get_pgconn(),
            "Charlie",
            "Not really constipated",
            {"birthdate": "2005-04-06"})


if __name__ == "__main__":
    unittest.main()
