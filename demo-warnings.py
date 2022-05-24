

import logging
logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger("demo")

import priorityprefix
priorityprefix.install()

import warnings


warnings.warn("This is a user warning")
warnings.warn("This is a deprecation warning", DeprecationWarning)
warnings.warn("This is a resource warning", ResourceWarning)  # ignored by default
