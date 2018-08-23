# vim: set expandtab ts=4 sw=4 filetype=python:

import json
import logging
import random
import re
import string
import textwrap
import uuid
import datetime

import psycopg2
from stuhlgang.webapp.framework.handler import Handler
from stuhlgang.webapp.framework.response import Response
from stuhlgang.model import message, session, user
from stuhlgang.model.user import PasswordHistory as password_history

from stuhlgang.model import numberoffailedloginattemps as loginattempt
from stuhlgang.webapp.auth import scrubbers

log = logging.getLogger(__name__)

"""

POST /api/sign-up
[email_address, display_name, password]

POST /api/start-session
[email_address, password]

GET /api/verify-session

POST /api/confirm-email

POST /api/end-session

"""

class StartSignup(Handler):

    route_strings = set ([
        "POST /api/signup",
        "POST /api/sign-up",
    ])

    route = Handler.check_route_strings

    required_json_keys = ["display_name", "email_address", "password"]

    def email_address_is_new(self, email_address):

        try:

            pg.people.Person.by_email_address(
                self.cw.get_pgconn(),
                email_address)

        except KeyError as ex:
            return True

        else:
            return False

    @staticmethod
    def email_is_valid(email_address):

        return bool(re.match(r".+@.+\..+", email_address))

    @Handler.require_json
    def handle(self, req):

		em = req.json["email_address"]

		if not self.email_is_valid(em):

			return Response.json(dict(
				success=False,
				reply_timestamp=datetime.datetime.now(),
				message="Sorry, {0} is not a valid email!".format(em)))

		elif not self.email_address_is_new(em):

			return Response.json(dict(
				success=False,
				reply_timestamp=datetime.datetime.now(),
				message="Sorry, Somebody else already signed up with "
					"email {0}!".format(em)))

		inserted_person = pg.people.Person.insert(
			self.cw.get_pgconn(),
			req.json["display_name"],
			em,
			req.json["password"])

		inserted_person.send_confirmation_code_via_email(
			self.cw.make_smtp_connection())

		return Response.json(dict(
			success=True,
			reply_timestamp=datetime.datetime.now(),
			inserted_person=inserted_person,
			message="Go check your email!"))
