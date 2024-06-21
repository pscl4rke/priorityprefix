
This Python module adds a prefix to log lines so that Journald
knows which log level it comes from.

Features:

* Can handle custom levels as well as Python's five standard ones.
* Ensures that each line of a multiline log message is correctly prefixed.
* Also applies a prefix to uncaught exceptions.
* And prefixes any messages from the `warnings` module.

## Usage in your Application

Install the latest stable version with

    $ pip install priorityprefix

Or install the cutting-edge version with

    $ pip install git+https://github.com/pscl4rke/priorityprefix.git

If you've already got a `Formatter` object for logging then you
can wrap it with `FormattingWrapper`:

    import priorityprefix
    my_formatter = priorityprefix.FormattingWrapper(my_formatter)

For lightweight usage there is an `install` function which integrates
nicely with `basicConfig` from the standard library

    import logging
    logging.basicConfig(level=logging.INFO)
    import priorityprefix
    priorityprefix.install()

By default `install()` will also override `sys.excepthook`
so that any uncaught exceptions will get an error priority prefix added to
their traceback before getting dumped to `stderr`.

Also, by default `install()` will also override `warnings.formatwarning`
so that things like a `DeprecationWarning` will get a warning priority prefix
before getting emitted.

Note that the `logging` library does not have a level that corresponds with
systemd's `NOTICE` level.
However you can create a custom level with a value of `25` to emit log
records that are notices:

    NOTICE = 25
    my_logger.log(NOTICE, "Message goes here")

## Usage with Journald

In short, you shouldn't need to change anything.

If setting up a Systemd service then you need to have the following
settings in your service definition:

    StandardOutput=journal
    StandardError=journal
    SyslogLevelPrefix=true

However these are the defaults,
so you don't normally need to change anything.

Similarly,
if you feed output through `systemd-cat`
(which fulfils the same role as `logger`)
then `--level-prefix` will also be enabled by default.

## The Back-Story

To get your log messages into Systemd's Journald you have a number of options:

* Send legacy Syslog datagrams to `/dev/log` and rely on Journald listening there
and translating them.
* Use something like `libsystemd` to send journal datagrams to `/run/systemd/journal/socket`.
* Just print stuff to `stdout` or `stderr`.  If Systemd has connected them up to the journal then each line will become a log record.

The last option is often the most popular because it's the easiest,
but the major downside is that you can't specify any custom fields.
You only have `MESSAGE` and the ones that Journald adds itself.

Except... you can precede lines with a special prefix to specify
the severity of the message.
This will be stripped off and turned into the `PRIORITY`.

| Prefix    | `PRIORITY`    |
|-----------|---------------|
| `<7>`     | Debug         |
| `<6>`     | Informational |
| `<5>`     | Notice        |
| `<4>`     | Warning       |
| `<3>`     | Error         |
| `<2>`     | Critical      |
| `<1>`     | Alert         |
| `<0>`     | Emergency     |

These prefices are
[inspired by Syslog](https://datatracker.ietf.org/doc/html/rfc5424#section-6.2.1),
although it only encodes priority levels and does not include facility data.

The purpose of this library is to automatically add these prefices to every
line of output.

## The Roadmap

In many respects this project is now complete.
Going forwards the things I want to achieve are:

* Maintain compatibility with new versions of Python as they get released.
Normally an annual thing.
* Support automatic enabling or disabling of the prefix based on whether
the `JOURNAL_STREAM` environment variable is present (supplied by Systemd)
or absent (when the user is running things from a terminal).
The complication of this is that the user would need to explicitly
enable the prefix any time they were piping into `systemd-cat`.

## Typechecking with Mypy et al

If you are checking the type annotations of your application you may
get an error about `priorityprefix` being skipped because of
missing stubs and markers.
This can be suppressed in Mypy with a special comment:

    import priorityprefix  # type: ignore

Some type annotations could be added to this library easily enough.
Unfortunately tools like Mypy adhere strictly to
[PEP 561](https://www.python.org/dev/peps/pep-0561/)
which requires the module to be fully refactored into a package
before it will be recognised.
Until a single-file module marker is available this library has
no way to communicate to the tooling that type information is available.

## Licence

This software library is released under the LGPL v3.0.
It may be used by and distributed with both GPL and non-GPL applications.
