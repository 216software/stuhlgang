# vim: set expandtab ts=4 sw=4 filetype=python:

import datetime
import logging
import textwrap

import decorator

from horsemeat.webapp import handler

from stuhlgang.webapp.framework.response import Response
from stuhlgang import pg

log = logging.getLogger(__name__)

module_template_prefix = 'framework'
module_template_package = 'stuhlgang.webapp.framework.templates'

class Handler(handler.Handler):

    # This might seem goofy, but it allows methods defined in horsemeat
    # to use our project's Response class.
    Response = Response

    @property
    def four_zero_four_template(self):
        return 'framework_templates/404.html'

    def not_found(self, req):

        return super(Handler, self).not_found(req)

    @staticmethod
    @decorator.decorator
    def get_session_from_cookie_or_json_or_QS(handler_method, self, req):

        """
        This thing sets the session attribute on the request object
        (req) from either the cookie, or from any JSON post data, or
        from a query string.

        I think the request object should figure the stuff about the
        different location of the session UUID, and then this decorator
        should only be in charge of just being a gatekeeper...

        You can test this like so::

            $ curl --data '{"session_uuid": "d5e19089-ce27-4ab9-b1d0-129a19c81a94"}' -H "Content-Type: application/json" http://circuit.xps/api/insert-club-fee

            $ curl http://circuit.xps/api/insert-club-fee?"session_uuid=d5e19089-ce27-4ab9-b1d0-129a19c81a94"

            $ curl 'http://circuit.xps/api/insert-club-fee' -H 'Cookie: session_uuid=d5e19089-ce27-4ab9-b1d0-129a19c81a94; session_hexdigest=162719e3a569b048b005d6d5140fe884'

        """

        found_session = False

        if req.user:
            found_session = True

        elif req.json and "session_uuid" in req.json:

            sesh = pg.sessions.Session.verify_session_uuid(
                self.cw.get_pgconn(),
                req.json["session_uuid"])

            if sesh:
                req.session = sesh
                found_session = True

        elif req.wz_req.args and "session_uuid" in req.wz_req.args:

            sesh = pg.sessions.Session.verify_session_uuid(
                self.cw.get_pgconn(),
                req.wz_req.args["session_uuid"])

            if sesh:
                req.session = sesh
                found_session = True

        if found_session:
            return handler_method(self, req)

        else:

            return Response.json(dict(
                reply_timestamp=datetime.datetime.now(),
                message="Sorry, you need to log in first!",
                needs_to_log_in=True,
                success=False))
