# vim: set expandtab ts=4 sw=4 filetype=python fileencoding=utf8:

import datetime
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

        charlie = pg.patients.Patient.insert(
            self.cw.get_pgconn(),
            "Charlie",
            "Not really constipated",
            {"birthdate": "2005-04-06"})

        self.assertEqual(charlie.display_name, "Charlie")
        self.assertEqual(charlie.extra_data, {"birthdate": "2005-04-06"})

        oliver = pg.patients.Patient.insert(
            self.cw.get_pgconn(),
            "Oliver",
            "Constipated!",
            {"birthdate": "2009-01-03"})

        susanna = pg.patients.Patient.insert(
            self.cw.get_pgconn(),
            "Susanna",
            "Not really!",
            {"birthdate": "2011-10-14"})

        james = pg.patients.Patient.insert(
            self.cw.get_pgconn(),
            "James",
            "???",
            {"birthdate": "2018-07-05"})


    def test_add_patient_events(self):

        oliver = pg.patients.Patient.insert(
            self.cw.get_pgconn(),
            "Oliver",
            "Constipated!",
            {"birthdate": "2009-01-03"})

        stored_event1 = pg.patients.PatientEvent.insert(
            self.cw.get_pgconn(),
            oliver.patient_number,
            datetime.datetime.now(),
            self.matt.person_uuid,
            "Very little",
            {"a":"99"})

        stored_event2 = pg.patients.PatientEvent.insert(
            self.cw.get_pgconn(),
            oliver.patient_number,
            datetime.datetime.now(),
            self.matt.person_uuid,
            "HUGE",
            {"a":"100"})

        self.assertNotEqual(
            stored_event1.event_timestamp,
            stored_event2.event_timestamp)

        stored_event3 = pg.patients.PatientEvent.insert(
            self.cw.get_pgconn(),
            oliver.patient_number,
            datetime.datetime.now(),
            self.matt.person_uuid,
            "small",
            {"a":"100"})

        susanna = pg.patients.Patient.insert(
            self.cw.get_pgconn(),
            "Susanna",
            "Not really!",
            {"birthdate": "2011-10-14"})

        susanna_event = pg.patients.PatientEvent.insert(
            self.cw.get_pgconn(),
            susanna.patient_number,
            datetime.datetime.now(),
            self.matt.person_uuid,
            "HUGE",
            {"a":"100"})

        oliver_events = list(pg.patients.PatientEvent.by_patient_number(
            self.cw.get_pgconn(),
            oliver.patient_number,
            0,
            100))

        self.assertEqual(len(oliver_events), 3)

        oliver_event_count = pg.patients.PatientEvent.count_patient_events(
            self.cw.get_pgconn(),
            oliver.patient_number)

        self.assertEqual(oliver_event_count, len(oliver_events))

        susanna_events = list(pg.patients.PatientEvent.by_patient_number(
            self.cw.get_pgconn(),
            susanna.patient_number,
            0,
            100))

        self.assertEqual(len(susanna_events), 1)

        susanna_event_count = pg.patients.PatientEvent.count_patient_events(
            self.cw.get_pgconn(),
            susanna.patient_number)

        self.assertEqual(susanna_event_count, len(susanna_events))

        oliver_event_subset = list(pg.patients.PatientEvent.by_patient_number(
            self.cw.get_pgconn(),
            oliver.patient_number,
            0,
            1))

        self.assertEqual(len(oliver_event_subset), 1)

        self.assertEqual(
            stored_event3.patient_event_number,
            oliver_event_subset[0].patient_event_number)

        oliver_event_subset = list(pg.patients.PatientEvent.by_patient_number(
            self.cw.get_pgconn(),
            oliver.patient_number,
            1,
            2))

        self.assertEqual(len(oliver_event_subset), 2)

        self.assertEqual(
            stored_event2.patient_event_number,
            oliver_event_subset[0].patient_event_number)

        self.assertEqual(
            stored_event1.patient_event_number,
            oliver_event_subset[1].patient_event_number)

if __name__ == "__main__":
    unittest.main()
