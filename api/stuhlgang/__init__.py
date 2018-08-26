# vim: set expandtab ts=4 sw=4 filetype=python fileencoding=utf8:

import logging
import functools
import json

from horsemeat import HorsemeatJSONEncoder

log = logging.getLogger(__name__)

class StuhGangJSONEncoder(HorsemeatJSONEncoder):

    """
    Each project can modify this just for fun if they want.
    """

    def default(self, obj):

        return super(StuhGangJSONEncoder, self).default(obj)


# TODO: add a docstring on this guy.
fancyjsondumps = functools.partial(
    json.dumps,
    cls=StuhGangJSONEncoder,
    sort_keys=True,
    indent=4,
    separators=(',', ': '))
