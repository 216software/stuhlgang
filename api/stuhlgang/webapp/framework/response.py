# vim: set expandtab ts=4 sw=4 filetype=python fileencoding=utf8:

import logging
import pprint

import clepy
from horsemeat.webapp import response

from stuhlgang import fancyjsondumps
from stuhlgang import configwrapper

log = logging.getLogger(__name__)

class Response(response.Response):

    """
    The Sthuhlgang response ALWAYS adds an extra header.
    """

    configwrapper = configwrapper
    fancyjsondumps = fancyjsondumps

    def __init__(self, status, headers, body):

        super(Response, self).__init__(status, headers, body)

        for h in [
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Credentials', 'true'),
            ("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Engaged-Auth-Token"),
        ]:

            self.headers.append(h)
