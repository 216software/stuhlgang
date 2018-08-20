# vim: set expandtab ts=4 sw=4 filetype=python fileencoding=utf8:

import logging
import re
import textwrap

from stuhlgang.webapp.framework.handler import Handler
from stuhlgang.webapp.framework.response import Response

__all__ = ["Splash"]

log = logging.getLogger(__name__)

module_template_prefix = 'mockups'
module_template_package = 'stuhlgang.webapp.mockups.templates'


class Splash(Handler):

    route_strings = set(['GET /'])

    route = Handler.check_route_strings

    def handle(self, req):

        return Response.tmpl('mockups/splash.html')
