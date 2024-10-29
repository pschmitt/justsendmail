#!/usr/bin/env python
# coding: utf-8

import argparse
import logging
import os
import ssl as ssllib
import sys
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP, SMTP_SSL
from typing import Any, Dict, Iterable, List, Optional, Union

from myldiscovery import autodiscover
from rich.console import Console
from rich.logging import RichHandler
from rich_argparse import RichHelpFormatter

LOGGER = logging.getLogger(__name__)


class AutoDiscoveryError(Exception):
    pass


def send_mail(
    sender: str,
    recipient: Union[str, List[str]],
    subject: str,
    message: str,
    attachments: Optional[
        Union[Dict[os.PathLike, os.PathLike], Iterable[os.PathLike]]
    ] = None,
    smtp_server: Optional[str] = "smtp.gmail.com",
    smtp_port: Optional[int] = 25,
    ssl: Optional[bool] = True,
    starttls: Optional[bool] = False,
    insecure: Optional[bool] = False,
    username: Optional[str] = None,
    password: Optional[str] = None,
    autodiscovery: bool = True,
) -> Any:
    if autodiscovery:
        settings = autodiscover(sender, username, password)
        smtp_settings = settings.get("smtp")
        if not smtp_settings:
            raise AutoDiscoveryError("SMTP settings not found")
        LOGGER.debug("Discovered SMTP settings: {}".format(smtp_settings))
        smtp_server = smtp_settings.get("server")
        smtp_port = smtp_settings.get("port")
        tls = smtp_settings.get("starttls")
        ssl = not tls
    LOGGER.debug(
        "Send mail via {}:{} (ssl: {}, starttls: {}) From: {} To: {}".format(
            smtp_server, smtp_port, ssl, starttls, sender, recipient
        )
    )
    msg = MIMEMultipart()

    if isinstance(recipient, list):
        if len(recipient) > 1:
            recipients = recipient
        else:
            # Comma separated recipient list
            if "," in recipient[0]:
                recipients = [x.strip() for x in recipient[0].split(",")]
            # Single recipient
            else:
                recipients = recipient
    else:
        # Comma separated recipient list
        if "," in recipient:
            recipients = [x.strip() for x in recipient.split(",")]
        # Single recipient
        else:
            recipients = [recipient]

    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)  # msg['To'] can only contain a string

    body = MIMEText(message)
    msg.attach(body)

    if attachments:
        if not isinstance(attachments, dict):
            attachments = {att: att for att in attachments}
        for k, v in attachments.items():
            part = MIMEBase("application", "octet-stream")
            part.set_payload(open(v, "rb").read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                'attachment; filename="{}"'.format(os.path.basename(k)),
            )
            msg.attach(part)

    LOGGER.debug(msg)

    ctx = ssllib.create_default_context()
    if insecure:
        ctx.check_hostname = False
        ctx.verify_mode = ssllib.CERT_NONE
    s = (
        SMTP_SSL(
            smtp_server,
            port=smtp_port,
            context=ctx,
        )
        if ssl
        else SMTP(smtp_server, port=smtp_port)
    )

    if starttls:
        # NOTE It might not make that much sense to do SSL, and then STARTTLS
        # on top of it.
        s.starttls(context=ctx)

    if password:
        user = username if username else sender
        s.login(user, password)

    res = s.sendmail(sender, recipients, msg.as_string())
    LOGGER.debug(f"sendmail result: {res}")
    s.quit()
    # res should be None. Unless some some recipients mailbox refused the mail
    # See upstream doc for more information
    return res


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Process args", formatter_class=RichHelpFormatter
    )
    parser.add_argument(
        "-N",
        "--no-autodiscovery",
        required=False,
        action="store_true",
        default=False,
        help="Disable autodiscovery of SMTP settings",
    )
    parser.add_argument(
        "-S",
        "--smtp",
        required=False,
        action="store",
        default="smtp.gmail.com",
        help="SMTP Server",
    )
    parser.add_argument(
        "-P",
        "--port",
        required=False,
        action="store",
        default=25,
        type=int,
        help="SMTP Server Port",
    )
    parser.add_argument(
        "--ssl",
        required=False,
        default=True,
        action="store_true",
        help="Use SSL/TLS",
    )
    parser.add_argument(
        "--starttls",
        required=False,
        default=False,
        action="store_true",
        help="Use STARTTLS",
    )
    parser.add_argument(
        "--insecure",
        required=False,
        default=False,
        action="store_true",
        help="Disable SSL/TLS certificate validation",
    )
    parser.add_argument(
        "-s",
        "--sender",
        required=True,
        action="store",
        help="Email of the sender",
    )
    parser.add_argument(
        "-u",
        "--username",
        required=False,
        default=None,
        action="store",
        help="Username of the account (default: sender email)",
    )
    parser.add_argument(
        "-p",
        "--password",
        required=False,
        default=None,
        action="store",
        help="Password of the account",
    )
    parser.add_argument(
        "-r",
        "--recipient",
        action="append",
        required=True,
        help="Recipient of the mail",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="Verbose output",
    )
    parser.add_argument(
        "-D", "--debug", action="store_true", help=argparse.SUPPRESS
    )
    parser.add_argument(
        "-a",
        "--attachment",
        action="append",
        required=False,
        type=argparse.FileType("r"),
        help="Attachment",
    )
    parser.add_argument("SUBJECT")
    parser.add_argument("MESSAGE")
    return parser.parse_args()


def main() -> int:
    console = Console()
    args = parse_args()
    logging.basicConfig(
        format="%(message)s",
        handlers=[RichHandler(console=console, rich_tracebacks=True)],
        level=logging.DEBUG if args.debug else logging.INFO,
    )
    LOGGER.debug(args)

    attachments = {}
    if args.attachment:
        for a in args.attachment:
            attachments[a.name] = a.name
    try:
        send_mail(
            autodiscovery=not args.no_autodiscovery,
            smtp_server=args.smtp,
            smtp_port=args.port,
            sender=args.sender,
            username=args.username,
            password=args.password,
            recipient=args.recipient,
            subject=args.SUBJECT,
            message=args.MESSAGE,
            attachments=attachments,
            starttls=args.starttls,
            ssl=args.ssl,
        )
        return 0
    except Exception:
        console.print_exception(show_locals=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
