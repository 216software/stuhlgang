# vim: set expandtab ts=4 sw=4 filetype=python:

import datetime
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
from stuhlgang import pg

log = logging.getLogger(__name__)

class VerifySessionUUID(Handler):

    route_strings = set(["GET /api/verify-session-uuid"])
    route = Handler.check_route_strings

    def handle(self, req):

        session_from_qs = None

        if not req.session and "session_uuid" in req.wz_req.args:

            try:

                session_uuid = uuid.UUID(req.wz_req.args["session_uuid"])

            except ValueError as ex:

                return Response.json(dict(
                    reply_timestamp=datetime.datetime.now(),
                    success=False,
                    message="Invalid UUID: {0}!".format(
                        req.wz_req.args["session_uuid"])))

            else:

                session_from_qs = pg.sessions.Session.verify_session_uuid(
                    self.cw.get_pgconn(),
                    session_uuid)

        if session_from_qs or req.session:

            sesh = session_from_qs or req.session

            logged_in_person = pg.people.Person.by_person_uuid(
                self.cw.get_pgconn(),
                sesh.person_uuid)

            resp = Response.json(dict(
                reply_timestamp=datetime.datetime.now(),
                success=True,
                message="Verified session is good until {0}.".format(
                    sesh.expires),
                session=sesh,
                logged_in_person=logged_in_person))

            resp.set_session_cookie(
                sesh.session_uuid,
                self.cw.app_secret)

            return resp

        else:

            return Response.json(dict(
                reply_timestamp=datetime.datetime.now(),
                success=False,
                message="Could not verify session"))

class AuthenticateWithEmailAndPassword(Handler):

    route_strings = set([
        "POST /api/authenticate",
        "POST /api/log-in",
        "POST /api/login",
        "POST /api/start-session"])

    route = Handler.check_route_strings

    required_json_keys = ["email_address", "password"]

    @Handler.require_json
    def handle(self, req):

        email_address = req.json["email_address"]
        password = req.json["password"]

        session = None

        session = pg.sessions.Session.maybe_start_new_session_after_checking_email_and_password(
            self.cw.get_pgconn(),
            email_address.strip(),
            password)

        if session:

            person = pg.people.Person.by_person_uuid(
                self.cw.get_pgconn(),
                session.person_uuid)

            log.info("{0} just logged in.".format(person.display_name))

            resp = Response.json(dict(
                reply_timestamp=datetime.datetime.now(),
                message="Session created and will expire on {0}".format(
                    session.expires),
                success=True,
                session=session,
                person=person))

            resp.set_session_cookie(
                session.session_uuid,
                self.cw.app_secret)

            return resp

        else:

            log.info("Failed login attempt: {0} / {1}".format(
                email_address,
                password))

            return Response.json(dict(
                message="Sorry, couldn't authenticate!",
                reply_timestamp=datetime.datetime.now(),
                success=False))

class EndSession(Handler):

    route_strings = set(["POST /api/logout", "POST /api/end-session"])
    route = Handler.check_route_strings

    required_json_keys = ["session_uuid"]

    @Handler.require_json
    def handle(self, req):

        try:

            session = pg.sessions.Session.by_session_uuid(
                self.cw.get_pgconn(),
                req.json["session_uuid"])

        except KeyError:

            return Response.json(dict(
                message="Sorry, could not find session {0}!".format(req.json["session_uuid"]),
                reply_timestamp=datetime.datetime.now(),
                success=False))

        else:

            updated_session = session.end_session(self.cw.get_pgconn())

            return Response.json(dict(
                message="Ended session {0}.".format(session.session_uuid),
                reply_timestamp=datetime.datetime.now(),
                success=True,
                session=updated_session))


class StartSignup(Handler):

    route_strings = set ([
        "POST /api/signup",
        "POST /api/sign-up",
    ])

    route = Handler.check_route_strings

    required_json_keys = ["display_name", "email_address", "agreed_with_TOS"]

    @Handler.require_json
    def handle(self, req):

        if not pg.people.Person.email_is_valid(req.json["email_address"]):

            return Response.json(dict(
                success=False,
                reply_timestamp=datetime.datetime.now(),
                message="Sorry, {email_address} is not a valid email!".format(**req.json)))

        elif not pg.people.Person.email_address_is_new(
            self.cw.get_pgconn(),
            req.json["email_address"]):

            return Response.json(dict(
                success=False,
                reply_timestamp=datetime.datetime.now(),
                message="Sorry, Somebody else already registered "
                    "email {email_address}!".format(**req.json)))

        elif req.json["agreed_with_TOS"]:

            inserted_person = pg.people.Person.insert(
                self.cw.get_pgconn(),
                req.json["display_name"],
                req.json["email_address"],
                datetime.datetime.now())

            inserted_person.send_confirmation_code_via_email(
                self.cw.make_smtp_connection())

            return Response.json(dict(
                success=True,
                reply_timestamp=datetime.datetime.now(),
                inserted_person=inserted_person,
                message="Go check your email!"))

        else:

            return Response.json(dict(
                success=False,
                reply_timestamp=datetime.datetime.now(),
                inserted_person=inserted_person,
                message="Sorry, you must agree with the terms of service to use this application"))

class ConfirmMembership(Handler):

    route_strings = set([
        "POST /api/confirm-email"
    ])

    route = Handler.check_route_strings

    required_json_keys = ["email_address", "confirmation_code"]

    @Handler.require_json
    def handle(self, req):

        try:

            confirmed_person = pg.people.Person.confirm_email(
                self.cw.get_pgconn(),
                req.json["email_address"],
                req.json["confirmation_code"])

        except KeyError as ex:

            return Response.json(dict(
                success=False,

                # This is yucky, but I don't know what else to do.
                message=ex.args[0],

                reply_timestamp=datetime.datetime.now()))

        else:

            return Response.json(dict(
                confirmed_person=confirmed_person,
                success=True,
                message="You ({0}) are now confirmed!".format(confirmed_person.display_name),
                reply_timestamp=datetime.datetime.now()))


class OptionsHandler(Handler):

    def route(self, req):

        if req.REQUEST_METHOD == "OPTIONS":
            return self.handle

    def handle(self, req):

        resp = Response(
            "200 OK",
            [

                ('Access-Control-Allow-Origin', dict(req.wz_req.headers).get('Origin', '*')),
                ('Access-Control-Allow-Credentials', 'true'),
                ("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Engaged-Auth-Token"),
            ],
            [])

        return resp

class StartSessionWithConfirmCode(Handler):

    route_strings = set([
        "POST /api/start-session-with-confirmation-code"
    ])

    route = Handler.check_route_strings

    @Handler.require_json
    def handle(self, req):

        email_address = req.json["email_address"]
        password = req.json["confirmation_code"]

        session = None

        session = pg.sessions.Session.maybe_start_new_session_after_checking_email_and_password(
            self.cw.get_pgconn(),
            email_address.strip(),
            password)

        if session:

            person = pg.people.Person.by_person_uuid(
                self.cw.get_pgconn(),
                session.person_uuid)

            log.info("{0} just logged in.".format(person.display_name))

            resp = Response.json(dict(
                reply_timestamp=datetime.datetime.now(),
                message="Session created and will expire on {0}".format(
                    session.expires),
                success=True,
                session=session,
                person=person))

            resp.set_session_cookie(
                session.session_uuid,
                self.cw.app_secret)

            return resp

        else:

            log.info("Failed login attempt: {0} / {1}".format(
                email_address,
                password))

            return Response.json(dict(
                message="Sorry, couldn't authenticate!",
                reply_timestamp=datetime.datetime.now(),
                success=False))






