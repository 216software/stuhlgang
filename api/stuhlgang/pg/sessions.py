# vim: set expandtab ts=4 sw=4 filetype=python:

import logging
import textwrap

log = logging.getLogger(__name__)

class Session(object):

    def __init__(self, session_uuid, expires, person_id, news_message,
        redirect_to_url, inserted, updated):

        self.session_uuid = session_uuid
        self.expires = expires
        self.person_id = person_id
        self.news_message = news_message
        self.redirect_to_url = redirect_to_url
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
        return self.__dict__
