#vim: set expandtab ts=4 sw=4 filetype=python:

import logging

from stuhlgang.webapp.framework.handler import Handler
from stuhlgang.webapp.framework.response import Response

log = logging.getLogger(__name__)

module_template_prefix = 'notfound'
module_template_package = 'stuhlgang.webapp.notfound.templates'

__all__ = ['NotFound']

class NotFound(Handler):

    """
    This handler should be appended to the end of the handlers list
    in the dispatcher, since it will grab any request.
    """

    def route(self, req):
        return self.handle

    def handle(self, req):
        return self.not_found(req)

    @property
    def four_zero_four_template(self):
        return 'stuhlgang/404.html'
