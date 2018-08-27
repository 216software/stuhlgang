# vim: set expandtab ts=4 sw=4 filetype=python:

import logging
import re
import textwrap

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import psycopg2.extras

from stuhlgang.pg import RelationWrapper

log = logging.getLogger(__name__)

class PersonFactory(psycopg2.extras.CompositeCaster):

    def make(self, values):
        d = dict(zip(self.attnames, values))
        return Person(**d)

class Person(RelationWrapper):

    def __init__(self, person_uuid, email_address, salted_hashed_password,
        person_status, display_name, confirmation_code,
        confirmation_code_set, is_superuser,
        agreed_with_tos, inserted, updated):

        self.person_uuid = person_uuid
        self.email_address = email_address
        self.salted_hashed_password = salted_hashed_password
        self.person_status = person_status
        self.display_name = display_name
        self.is_superuser = is_superuser
        self.confirmation_code = confirmation_code
        self.confirmation_code_set = confirmation_code_set
        self.agreed_with_tos = agreed_with_tos
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

    @classmethod
    def insert(cls, pgconn, display_name, email_address, agreed_with_TOS):

        cursor = pgconn.cursor()

        cursor.execute(textwrap.dedent("""
            insert into people
            (display_name, email_address, agreed_with_TOS)
            values
            (%(display_name)s, %(email_address)s, %(agreed_with_TOS)s)
            returning people.*::people as inserted_person
            """), locals())

        return cursor.fetchone().inserted_person

    def send_confirmation_code_via_email(self, smtpconn):

        msg = MIMEMultipart('alternative')

        msg['Subject'] = "Confirm your Help Me 2 Poop membership!"
        msg['From'] = "support@helpme2poop.com"
        msg['To'] = self.email_address

        msg.attach(self.write_confirmation_email())

        smtpconn.sendmail(
            "support@helpme2poop.com",
            [self.email_address],
            msg.as_string())

        log.info(
            "Just sent confirmation email to {0}.".format(
                self.email_address))

    def write_confirmation_email(self):

        if not self.confirmation_code:
            raise ValueError("Sorry, I don't have a confirmation code!")

        else:

            from stuhlgang import configwrapper

            cw = configwrapper.ConfigWrapper.get_default()

            import locale
            locale.setlocale(locale.LC_ALL, '')

            html_tmpl = cw.j.get_template(
                "emailtemplates/confirm-signup.html")

            html_email = MIMEText(
                html_tmpl.render(
                    confirmation_code=self.confirmation_code,
                    person=self,
                    locale=locale),
                'html')

            return html_email

    def reset_confirmation_code(self, pgconn):

        cursor = pgconn.cursor()

        cursor.execute(textwrap.dedent("""
            update people
            set confirmation_code = to_char(random_between(1, 9999),
            'fm0000'),
            confirmation_code_set = current_timestamp
            where person_uuid = %(person_uuid)s
            returning people.*::people as updated_person
            """), dict(person_uuid=self.person_uuid))

        if cursor.rowcount:
            return cursor.fetchone().updated_person

        else:
            raise KeyError("Sorry, no person {0} found!".format(self.person_uuid))

    def set_confirmation_code(self, pgconn, new_code=None):

        cursor = pgconn.cursor()

        cursor.execute(textwrap.dedent("""
            update people
            set confirmation_code = %(new_code)s,

            confirmation_code_set = case when %(new_code)s is null then
            null else current_timestamp
            end

            where person_uuid = %(person_uuid)s
            returning people.*::people as updated_person
            """), dict(person_uuid=self.person_uuid, new_code=new_code))

        if cursor.rowcount:
            return cursor.fetchone().updated_person

        else:
            raise KeyError("Sorry, no person {0} found!".format(self.person_uuid))

    @staticmethod
    def email_address_is_new(pgconn, email_address):

        try:

            Person.by_email_address(pgconn, email_address)

        except KeyError as ex:
            return True

        else:
            return False

    @staticmethod
    def email_is_valid(email_address):

        return bool(re.match(r".+@.+\..+", email_address))


    def set_password(self, pgconn, new_password):

        cursor = pgconn.cursor()

        cursor.execute(textwrap.dedent("""
            update people
            set salted_hashed_password = crypt(%(new_password)s, gen_salt('bf'))
            where person_uuid = %(person_uuid)s
            returning people.*::people as updated_person
            """), dict(
                person_uuid=self.person_uuid,
                new_password=new_password))

        if cursor.rowcount:
            return cursor.fetchone().updated_person

        else:
            raise KeyError("Sorry, no person {0} found!".format(self.person_uuid))

    @classmethod
    def confirm_email(cls, pgconn, email_address, confirmation_code):

        """
        This means to mark this email address as confirmed.
        """

        cursor = pgconn.cursor()

        cursor.execute(textwrap.dedent("""
            update people
            set person_status = 'confirmed',
            confirmation_code = NULL
            where email_address = %(email_address)s
            and confirmation_code = %(confirmation_code)s
            returning people.*::people as confirmed_person
            """), locals())

        if cursor.rowcount:
            return cursor.fetchone().confirmed_person

        else:
            raise KeyError("Sorry, {0} doesn't match the confirmation code for email {1} " "!".format(
                confirmation_code,
                email_address))

