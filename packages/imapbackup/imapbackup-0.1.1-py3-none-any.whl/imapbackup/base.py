#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement

import ssl
import imaplib
import logging

logger = logging.getLogger(__name__)
imap_login_expected = "OK"

def fix_imap_server_limit(maxline=1024*1024*1024):
    """The original server limit is 1000000, it's too small to download large email that not well formatted.
    """
    logger.info(f"imapbackup.base.fix_imap_server_limit, old_vlaue={imaplib._MAXLINE}, new_value={maxline}...")
    imaplib._MAXLINE = maxline

def get_imap_server(username, password, server, port=0, enable_ssl=False, ssl_ciphers="DEFAULT", timeout=None):
    """Create IMAP server instance.
    """
    # python 3.8 and below, imaplib.IMAP4 and imaplib.IMAP4_SSL doesn't support timeout parameter
    # so we set the socket's default timeout instead
    if timeout:
        import socket
        socket.setdefaulttimeout(timeout)

    logger.debug(f"get_imap_server start: username={username}, password=***, server={server}, port={port}, enable_ssl={enable_ssl}, ssl_ciphers={ssl_ciphers}, timeout={timeout}...")
    if port == 0:
        if enable_ssl:
            port = 993
        else:
            port = 143
    if enable_ssl:
        ssl_context = ssl._create_unverified_context()
        ssl_context.set_ciphers(ssl_ciphers)
        instance = imaplib.IMAP4_SSL(server, port, ssl_context=ssl_context)
    else:
        instance = imaplib.IMAP4(server, port)
    try:
        status, data = instance.login(username, password)
        msg = f"imapbackup.base.get_imap_server do user login success: username={username}, password=***, server={server}, port={port}, enable_ssl={enable_ssl}, ssl_ciphers={ssl_ciphers}, timeout={timeout}, status={status}, data={data}..."
        logger.debug(msg)
    except Exception as error:
        status, data = "FAILED", [error]
    if status != imap_login_expected:
        msg = f"imapbackup.base.get_imap_server do user login failed: username={username}, password=***, server={server}, port={port}, enable_ssl={enable_ssl}, ssl_ciphers={ssl_ciphers}, timeout={timeout}, status={status}, data={data}..."
        logger.error(msg)
        raise Exception(msg)
    return instance


fix_imap_server_limit()
