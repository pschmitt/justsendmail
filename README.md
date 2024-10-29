# Justsendmail

[![PyPI](https://img.shields.io/pypi/v/justsendmail)](https://pypi.org/project/justsendmail/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/justsendmail)](https://pypi.org/project/justsendmail/)
[![PyPI - License](https://img.shields.io/pypi/l/justsendmail)](https://pypi.org/project/justsendmail/)
[![Python Lint](https://github.com/pschmitt/justsendmail/workflows/Python%20Lint/badge.svg)](https://github.com/pschmitt/justsendmail/actions?query=workflow%3A%22Python+Lint%22)

Simple CLI tool to send mail using Python 3+

## Installation

```
pip install justsendmail

# or with pipx:
pipx install justsendmail
```

## Usage

```
$ justsendmail --help
usage: justsendmail [-h] [-N] [-S SMTP] [-P PORT] [--tls] -s SENDER
                    [-u USERNAME] [-p PASSWORD] -r RECIPIENT [-v]
                    [-a ATTACHMENT]
                    SUBJECT MESSAGE

Process args

positional arguments:
  SUBJECT
  MESSAGE

options:
  -h, --help            show this help message and exit
  -N, --no-autodiscovery
                        Disable autodiscovery of SMTP settings
  -S SMTP, --smtp SMTP  SMTP Server
  -P PORT, --port PORT  SMTP Server Port
  --tls                 Use TLS
  -s SENDER, --sender SENDER
                        Email of the sender
  -u USERNAME, --username USERNAME
                        Username of the account (default: sender email)
  -p PASSWORD, --password PASSWORD
                        Password of the account
  -r RECIPIENT, --recipient RECIPIENT
                        Recipient of the mail
  -v, --verbose         Verbose output
  -a ATTACHMENT, --attachment ATTACHMENT
                        Attachment
```
