import logging

# Libraries must not install handlers or impose levels on the application that
# imports them. A NullHandler keeps the "no handler configured" case silent
# instead of letting records fall through to logging.lastResort (stderr).
logging.getLogger(__name__).addHandler(logging.NullHandler())


def set_log_level(level):
    """Set the level of every pycryptotools logger at once.

    All modules log to `pycryptotools.<module>` and none of them set their own
    level, so setting it here cascades to all of them. This is the supported
    way for an application to turn pycryptotools logging up or down.
    """
    logging.getLogger(__name__).setLevel(level)


from .blocks import *
from .composite import *
from .deterministic import *
from .main import *
from .mnemonic import *
from .py2specials import *
from .py3specials import *
from .stealth import *
from .transaction import *
#from .coins import *
from .keystore import *
from .wallet import *
