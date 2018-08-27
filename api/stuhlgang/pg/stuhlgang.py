# vim: set expandtab ts=4 sw=4 filetype=python fileencoding=utf8:

import logging
import re
import textwrap

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import psycopg2.extras

from stuhlgang.pg import RelationWrapper

log = logging.getLogger(__name__)

class PatientFactory(psycopg2.extras.CompositeCaster):

    def make(self, values):
        d = dict(zip(self.attnames, values))
        return Patient(**d)

class Patient(RelationWrapper):

    def __init__(self, patient_number, display_name, extra_notes,
        extra_data, inserted, updated):

        self.patient_number = patient_number
        self.display_name = display_name
        self.extra_notes = extra_notes
        self.extra_data = extra_data
        self.inserted = inserted
        self.updated = updated

    @classmethod
    def patients_for_caretaker(cls, pgconn, caretaker_uuid, offset, limit):

        cursor = pgconn.cursor()

        cursor.execute(textwrap.dedent("""
            select patients.*::patients as patient
            from patients
            join patient_caretakers
            on patients.patient_number = patient_caretakers.patient_number
            and patient_caretakers.caretaker = %(caretaker_uuid)s
            order by patients.display_name
            offset %(offset)s
            limit %(limit)s
            """), locals())

        for row in cursor:
            yield row.patient

    @classmethod
    def patients_for_hcprovider(cls, pgconn, provider_uuid, offset, limit):

        cursor = pgconn.cursor()

        cursor.execute(textwrap.dedent("""
            select patients.*::patients as patient
            from patients
            join provider_patient_links
            on patients.patient_number = patient_caretakers.patient_number
            and provider_patient_links.provider = %(provider_uuid)s
            order by patients.display_name
            offset %(offset)s
            limit %(limit)s
            """), locals())

        for row in cursor:
            yield row.patient

    # Just an alias
    patients_for_provider = patients_for_hcprovider

    @classmethod
    def insert(cls, pgconn, display_name, extra_notes, extra_data):

        j = psycopg2.extras.Json(extra_data)

        cursor = pgconn.cursor()

        cursor.execute(textwrap.dedent("""
            insert into patients
            (display_name, extra_notes, extra_data)
            values
            (%(display_name)s, %(extra_notes)s, %(j)s)
            returning patients.*::patients as inserted_patient
            """), locals())

        return cursor.fetchone().inserted_patient

    @staticmethod
    def link_to_caretaker(pgconn, patient_number, caretaker_uuid,
        extra_notes, extra_data):

        j = psycopg2.extras.Json(extra_data)

        cursor = pgconn.cursor()

        cursor.execute(textwrap.dedent("""
            insert into patient_caretakers
            (patient_number, caretaker, extra_notes, extra_data)
            values
            (%(patient_number)s, %(caretaker)s, %(extra_notes)s, %(j)s)
            returning patient_caretakers.*::patient_caretakers as
            patient_caretaker_link
            """), locals())

        return cursor.fetchone().patient_caretaker_link

    @staticmethod
    def link_to_provider(pgconn, patient_number, provider_uuid,
        extra_notes, extra_data):

        j = psycopg2.extras.Json(extra_data)

        cursor = pgconn.cursor()

        cursor.execute(textwrap.dedent("""
            insert into provider_patient_links
            (patient_number, provider, extra_notes, extra_data)
            values
            (%(patient_number)s, %(provider)s, %(extra_notes)s, %(j)s)
            returning provider_patient_links.*::provider_patient_links as provider_patient_link
            """), locals())

        return cursor.fetchone().patient_provider_link

    @staticmethod
    def verify_is_my_caretaker(pgconn, patient_number, caretaker_uuid):

        cursor = pgconn.cursor()

        cursor.execute(textwrap.dedent("""
            select patient_caretakers.*::patient_caretakers as patient_caretaker_link
            from patient_caretakers
            where patient_number =  %(patient_number)s
            and caretaker = %(caretaker_uuid)s
            """), locals())

        if cursor.rowcount:
            return cursor.fetchone().patient_caretaker_link

class PatientEventFactory(psycopg2.extras.CompositeCaster):

    def make(self, values):
        d = dict(zip(self.attnames, values))
        return PatientEvent(**d)

class PatientEvent(RelationWrapper):

    def __init__(self, patient_event_number, patient_number, event_timestamp,
        stored_by, extra_notes, extra_data, inserted, updated):

        self.patient_event_number = patient_event_number
        self.patient_number = patient_number
        self.event_timestamp = event_timestamp
        self.stored_by = stored_by
        self.extra_notes = extra_notes
        self.extra_data = extra_data
        self.inserted = inserted
        self.updated = updated

    @classmethod
    def by_patient_number(cls, pgconn, patient_number, offset, limit):

        cursor = pgconn.cursor()

        cursor.execute(textwrap.dedent("""
            select patient_events.*::patient_events as pe
            from patient_events
            where patient_number = %(patient_number)s
            order by event_timestamp desc
            offset %(offset)s
            limit %(limit)s
            """), locals())

        for row in cursor:
            yield row.pe

    @classmethod
    def insert(cls, pgconn, patient_number, event_timestamp, extra_notes, extra_data):

        j = psycopg2.extras.Json(extra_data)

        cursor = pgconn.cursor()

        cursor.execute(textwrap.dedent("""
            insert into patient_events
            (patient_number, event_timestamp, extra_notes, extra_data)
            values
            (%(patient_number)s, %(event_timestamp)s, %(extra_notes)s, %(j)s)
            returning patient_events.*::patient_events as
            inserted_patient_event
            """), locals())

        return cursor.fetchone().inserted_patient_event

    @staticmethod
    def count_patient_events(pgconn, patient_number):

        cursor = pgconn.cursor()

        cursor.execute(textwrap.dedent("""
            select count(*)
            from patient_events
            where patient_number = %(patient_number)s
            """), locals())

        return cursor.fetchone().count
