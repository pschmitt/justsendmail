# Justsendmail

[![PyPI](https://img.shields.io/pypi/v/justsendmail)](https://pypi.org/project/justsendmail/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/justsendmail)](https://pypi.org/project/justsendmail/)
[![PyPI - License](https://img.shields.io/pypi/l/justsendmail)](https://pypi.org/project/justsendmail/)
[![Python Lint](https://github.com/pschmitt/justsendmail/workflows/Python%20Lint/badge.svg)](https://github.com/pschmitt/justsendmail/actions?query=workflow%3A%22Python+Lint%22)

Simple CLI tool to send mail using Python 3+

## Installation

```shell
pip install justsendmail

# or with pipx:
pipx install justsendmail
```

and there's this too 💑:

```shell
nix run 'git+https://github.com/pschmitt/nixos-config#justsendmail' -- --help
```

## Usage

```
$ justsendmail --help
Usage: justsendmail.py [-h] [-N] [-S SMTP] [-P PORT] [--ssl] [--starttls]
                       [--insecure] -s SENDER [-u USERNAME] [-p PASSWORD] -r
                       RECIPIENT [-v] [-a ATTACHMENT]
                       SUBJECT MESSAGE

Process args

Positional Arguments:
  SUBJECT
  MESSAGE

Options:
  -h, --help            show this help message and exit
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
