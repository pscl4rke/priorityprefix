

import logging
logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger("demo")

import priorityprefix
priorityprefix.install()

LOG.debug("I am a debug message")
LOG.info("I am an info message")
LOG.warning("I am a warning message")
LOG.error("I am an error message")
LOG.critical("I am a critical message")

def f():
    return g()
def g():
    return h()
def h():
    return int("I am not an int")

try:
    f()
except Exception as exc:
    LOG.exception(exc)
