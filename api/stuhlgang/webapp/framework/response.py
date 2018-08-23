# vim: set expandtab ts=4 sw=4 filetype=python fileencoding=utf8:

import logging
import pprint

import clepy
from horsemeat.webapp import response

from stuhlgang import fancyjsondumps

log = logging.getLogger(__name__)

class Response(response.Response):

    """
    Add stuff here that is specific to the stuhlgang response.
    """
