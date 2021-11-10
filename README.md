
This Python module adds a prefix to log lines so that Journald
knows which log level it comes from.

Features:

* Can handle custom levels as well as Python's five standard ones.
* Ensures that each line of a multiline log message is correctly prefixed.

## Usage in your Application

Install the cutting-edge version with

    $ pip install git+https://github.com/pscl4rke/priorityprefix.git

If you've aleady got a `Formatter` object for logging then you
can wrap it with `FormattingWrapper`:

    import priorityprefix
    my_formatter = priorityprefix.FormattingWrapper(my_formatter)

For lightweight usage there is an `install` function which integrates
nicely with `basicConfig` from the standard library

    import logging
    logging.basicConfig(level=logging.INFO)
    import priorityprefix
    priorityprefix.install()

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

## Licence

This software library is released under the LGPL v3.0.
It may be used by and distributed with both GPL and non-GPL applications.
