#vim: set expandtab ts=4 sw=4 filetype=python:

import datetime
import logging

from stuhlgang.webapp.framework.handler import Handler
from stuhlgang.webapp.framework.response import Response

log = logging.getLogger(__name__)

module_template_prefix = 'stuhlgang'
module_template_package = 'stuhlgang.webapp.stuhlgang.templates'

class Splash(Handler):

    route_strings = set(['GET /'])
    route = Handler.check_route_strings

    def handle(self, req):

        return Response.json(dict(
            message="Welcome to the StuhlGang API",
            success=True,
            reply_timestamp=datetime.datetime.now()))
