# vim: set expandtab ts=4 sw=4 filetype=python:

import copy
import datetime
import logging
import textwrap

import psycopg2.extras
import pytz

log = logging.getLogger(__name__)

from stuhlgang.pg import RelationWrapper

class SessionFactory(psycopg2.extras.CompositeCaster):

    def make(self, values):
        d = dict(zip(self.attnames, values))
        return Session(**d)

class Session(RelationWrapper):

    def __init__(self, session_uuid, expires, person_uuid,
        inserted, updated):

        self.session_uuid = session_uuid
        self.expires = expires
        self.person_uuid = person_uuid
        self.inserted = inserted
        self.updated = updated

    @classmethod
    def maybe_start_new_session_after_checking_email_and_password(cls,
        pgconn, email_address, password):

        """
        If the email address and password match a row in the people
        table, insert a new session and return it.
        """

        cursor = pgconn.cursor()

        cursor.execute(textwrap.dedent("""
            insert into webapp_sessions
            (person_uuid)
            select person_uuid
            from people
            where email_address = %(email_address)s
            and salted_hashed_password = crypt(
                %(password)s,
                salted_hashed_password)
            and person_status = 'confirmed'
            returning (webapp_sessions.*)::webapp_sessions as gs
            """), {
                "email_address": email_address,
                "password": password})

        if cursor.rowcount:
            return cursor.fetchone().gs

    def maybe_update_session_expires_time(self, pgconn):

        cursor = pgconn.cursor()

        cursor.execute(textwrap.dedent("""
            update webapp_sessions
            set expires = default
            where session_uuid = (%(session_uuid)s)
            and expires > current_timestamp
            returning expires
        """), {'session_uuid': self.session_uuid})

        if cursor.rowcount:
            return cursor.fetchone().expires

    @property
    def __jsondata__(self):

        d = copy.copy(self.__dict__)
        d["expired"] = self.expired
        return d

    @property
    def expired(self):
        return self.expires <= pytz.UTC.localize(datetime.datetime.utcnow())

    @classmethod
    def verify_session_uuid(cls, pgconn, session_uuid):

        """
        Returns the session only if it hasn't expired yet.
        """

        cursor = pgconn.cursor()

        cursor.execute(textwrap.dedent("""
            select webapp_sessions.*::webapp_sessions as session
            from webapp_sessions
            where session_uuid = %(session_uuid)s
            and expires >= current_timestamp
            """), locals())

        if cursor.rowcount:
            return cursor.fetchone().session

    by_valid_session_uuid = verify_session_uuid

    def end_session(self, pgconn):

        cursor = pgconn.cursor()

        cursor.execute(textwrap.dedent("""
            update webapp_sessions
            set expires = current_timestamp
            where session_uuid = (%(session_uuid)s)
            returning webapp_sessions.*::webapp_sessions as session
        """), {'session_uuid': self.session_uuid})

        if cursor.rowcount:
            return cursor.fetchone().session

    @classmethod
    def by_session_uuid(cls, pgconn, session_uuid):

        cursor = pgconn.cursor()

        cursor.execute(textwrap.dedent("""
            select webapp_sessions.*::webapp_sessions as session
            from webapp_sessions
            where session_uuid = %(session_uuid)s
            """), locals())

        if cursor.rowcount:
            return cursor.fetchone().session

        else:
            raise KeyError(
                "Could not find any session with session UUID {0}.".format(
                    session_uuid))
