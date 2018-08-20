# vim: set expandtab ts=4 sw=4 filetype=python:

import logging
import textwrap

import psycopg2.extras

log = logging.getLogger(__name__)

class PersonFactory(psycopg2.extras.CompositeCaster):

    def make(self, values):
        d = dict(zip(self.attnames, values))
        return Person(**d)

class Person(object):

    def __init__(self, person_uuid, email_address, salted_hashed_password,
        person_status, display_name, inserted, updated):

        self.person_uuid = person_uuid
        self.email_address = email_address
        self.salted_hashed_password = salted_hashed_password
        self.person_status = person_status
        self.display_name = display_name
        self.is_superuser = is_superuser
        self.is_institution_superuser = is_institution_superuser
        self.did_acknowledge_eula = did_acknowledge_eula
        self.challenge_question = challenge_question
        self.challenge_question_answer = challenge_question_answer
        self.date_password_changed=date_password_changed
        self.inserted = inserted
        self.updated = updated

    def __repr__(self):
        return '<{0}.{1} ({2}:{3}) at 0x{4:x}>'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.person_uuid,
            self.display_name,
            id(self))

    def __eq__(self, other):
        return self.person_uuid == getattr(other, 'person_uuid', -1)

    @classmethod
    def by_email_address(cls, pgconn, email_address):

        cursor = pgconn.cursor()

        cursor.execute(textwrap.dedent("""
            select (p.*)::people as p
            from people p
            where email_address = %(email_address)s
            """), {'email_address': email_address})

        if cursor.rowcount:
            return cursor.fetchone().p

        else:
            raise KeyError("Sorry, couldn't find {0}!".format(
                email_address))

    @property
    def __jsondata__(self):

        return {k:v for (k, v) in self.__dict__.items()
            if k in set([
                'display_name',
                'email_address',
                'person_uuid'])}

    @classmethod
    def by_person_uuid(cls, pgconn, person_uuid):

        cursor = pgconn.cursor()

        cursor.execute(textwrap.dedent("""
            select (p.*)::people as p
            from people p
            where person_uuid = %(person_uuid)s
            """), {'person_uuid': person_uuid})

        if cursor.rowcount:
            return cursor.fetchone().p
