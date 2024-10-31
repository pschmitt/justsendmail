> [!WARNING]
> This package has been renamed to [`sendmyl`](https://pypi.org/project/sendmyl/).
>
> Please update your dependencies accordingly.

# sendmyl

[![PyPI](https://img.shields.io/pypi/v/sendmyl)](https://pypi.org/project/sendmyl/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/sendmyl)](https://pypi.org/project/sendmyl/)
[![PyPI - License](https://img.shields.io/pypi/l/sendmyl)](https://pypi.org/project/sendmyl/)
[![Python Lint](https://github.com/pschmitt/sendmyl/workflows/Python%20Lint/badge.svg)](https://github.com/pschmitt/sendmyl/actions?query=workflow%3A%22Python+Lint%22)

Simple CLI tool to send mail using Python 3+

## Installation

```shell
pip install sendmyl

# or with pipx:
pipx install sendmyl
```

and there's this too 💑:

```shell
nix run github:pschmitt/sendmyl -- --help
```

## Usage

```
Usage: sendmyl [-h] [-V] [-N] [-S SMTP] [-P PORT] [--ssl] [--starttls]
               [--insecure] -s SENDER [-u USERNAME] [-p PASSWORD] -r
               RECIPIENT [-v] [-a ATTACHMENT]
               SUBJECT MESSAGE

Process args

Positional Arguments:
  SUBJECT
  MESSAGE

Options:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -N, --no-autodiscovery
                        Disable autodiscovery of SMTP settings
  -S, --smtp SMTP       SMTP Server
  -P, --port PORT       SMTP Server Port
  --ssl                 Use SSL/TLS
  --starttls            Use STARTTLS
  --insecure            Disable SSL/TLS certificate validation
  -s, --sender SENDER   Email of the sender
  -u, --username USERNAME
                        Username of the account (default: sender email)
  -p, --password PASSWORD
                        Password of the account
  -r, --recipient RECIPIENT
                        Recipient of the mail
  -v, --verbose         Verbose output
  -a, --attachment ATTACHMENT
                        Attachment
```
