# vim: set expandtab ts=4 sw=4 filetype=python:

import logging
import textwrap

from horsemeat.webapp import handler

from stuhlgang.webapp.framework.response import Response

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

