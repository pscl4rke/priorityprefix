

import logging
logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger("demo")

import priorityprefix
priorityprefix.install()


def f():
    try:
        return g()
    except Exception as exc:
        msg = "Wrapping Exception"
        raise Exception(msg) from exc


def g():
    return h()


def h():
    return int("I am not an int")


# Will throw an uncaught error
f()
