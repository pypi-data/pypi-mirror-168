#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement

import os
import logging

import click
from zenutils import logutils
from tabulate import tabulate

from .base import get_imap_server
from .mailbox import Mailbox

logger = logging.getLogger(__name__)

@click.group()
@click.option("--username", help="IMAP account username.", required=True)
@click.option("--password", help="IMAP account password.", required=True)
@click.option("--host", help="IMAP server host.", required=True)
@click.option("--port", type=int, default=0, help="IMAP server port, default to 993 if SSL is enabled and default to 143 if SSL is not enabled.")
@click.option("--ssl/--no-ssl", is_flag=True, default=True, help="Enable ssl.")
@click.option("--ssl-ciphers", default="DEFAULT", help="SSL ciphers used to make SSL connection.")
@click.option("--connection-timeout", type=int, help="Connection timeout.")
@click.option("--loglevel", type=click.Choice(["DEBUG", "INFO", "WARN", "ERROR"]), default="INFO")
@click.option("--logfmt", type=click.Choice(["default", "simple", "message_only"]), default="simple")
@click.pass_context
def main(ctx, host, port, ssl, username, password, ssl_ciphers, connection_timeout, loglevel, logfmt):
    ctx.ensure_object(dict)
    ctx.obj['host'] = host
    ctx.obj['port'] = port
    ctx.obj['ssl'] = ssl
    ctx.obj['username'] = username
    ctx.obj['password'] = password
    ctx.obj['ssl_ciphers'] = ssl_ciphers
    ctx.obj['connection_timeout'] = connection_timeout
    logutils.setup(loglevel=loglevel, logfmt=logfmt, root={
        "handlers": [logfmt+"_file"],
    })
    logger.debug("imapbackup.main start...")

@main.command("backup")
@click.option("-l", "--limit", type=int, default=0, help="Fetch limit.")
@click.option("-d", "--dest", default="data", help="Dest folder. Data storage root. Default to ./data/.")
@click.option("-n", "--no-subject-title", help="Default title name used when the email has NO subject.")
@click.argument("folder", nargs=-1, required=False)
@click.pass_context
def do_backup_folder(ctx, limit, dest, no_subject_title, folder):
    """Backup folders from IMAP server. If no folder given, then backup all folders.
    
    Data save structure:

    ----------------------------------------------------------

    <Dest>

        <MailFolder 1>

            <mail_uid>-<mail_date>-<mail_subject>-<mail_body_hashcode>.eml

        <MailFolder ...>

            <mail_uid>-<mail_date>-<mail_subject>-<mail_body_hashcode>.eml

    ----------------------------------------------------------

    <Dest>: is your data storage root. Given by option -d.

    <MailFolder>: is the folder name from the IMAP server.

    <mail_uid>: is the mail's UID from the IMAP server.

    <mail_date>: is the mail's INTERNALDATE from the IMAP server.

    <mail_subject>: is the mail's Subject. We replace slash “/” sign to underline "_" sign.

    <mail_body_hashcode>: is the sha1 hash code of the mail's BODY.

    ----------------------------------------------------------
    """
    logger.debug("imapbackup.do_backup_folder start...")
    username = ctx.obj["username"]
    password = ctx.obj["password"]
    host = ctx.obj["host"]
    port = ctx.obj["port"]
    ssl = ctx.obj["ssl"]
    ssl_ciphers = ctx.obj["ssl_ciphers"]
    connection_timeout = ctx.obj["connection_timeout"]
    logger.debug(f"imapbackup.do_backup_folder connect to IMAP server start...")
    server = get_imap_server(username, password, host, port, enable_ssl=ssl, ssl_ciphers=ssl_ciphers, timeout=connection_timeout)
    logger.debug(f"imapbackup.do_backup_folder connect to IMAP server success: server={server}...")
    mailbox = Mailbox(server)
    if no_subject_title:
        mailbox.no_subject_title = no_subject_title
    if folder:
        folders = folder
    else:
        folders = [x[0] for x in mailbox.get_all_folders()]
    result = []
    for folder in folders:
        info = mailbox.backup(dest, folder, limit=limit)
        result.append((folder, info))

    table = []
    for folder, info in result:
        row = [folder]
        for c in info:
            row.append(c)
        table.append(row)
    print(tabulate(table, headers=["Folder", "Downloaded", "Failed", "New", "Total"]))

@main.command("list")
@click.option("--folder-name-max-length", type=int, default=0)
@click.option("--folder-name-mask", default=" ")
@click.pass_context
def do_list_folders(ctx, folder_name_max_length, folder_name_mask):
    """List all folders of the IMAP server.
    """
    logger.debug("imapbackup.do_list_folders start...")
    username = ctx.obj["username"]
    password = ctx.obj["password"]
    host = ctx.obj["host"]
    port = ctx.obj["port"]
    ssl = ctx.obj["ssl"]
    ssl_ciphers = ctx.obj["ssl_ciphers"]
    connection_timeout = ctx.obj["connection_timeout"]
    logger.debug(f"imapbackup.do_list_folders connect to IMAP server start...")
    server = get_imap_server(username, password, host, port, enable_ssl=ssl, ssl_ciphers=ssl_ciphers, timeout=connection_timeout)
    logger.debug(f"imapbackup.do_list_folders connect to IMAP server success: server={server}...")
    mailbox = Mailbox(server)
    folders = mailbox.get_all_folders()
    table = []
    for name, path in folders:
        table.append([name, path])
    print(tabulate(table, headers=["Folder", "Path"]))

@main.command("upload")
@click.option("-f", "--folder", default="INBOX", help="Upload eml to this folder. The folder MUST be created already. Default to INBOX.")
@click.argument("data", nargs=-1, required=True)
@click.pass_context
def do_upload_eml(ctx, folder, data):
    """Upload eml to IMAP server.
    """
    logger.debug("imapbackup.do_upload_eml start...")
    username = ctx.obj["username"]
    password = ctx.obj["password"]
    host = ctx.obj["host"]
    port = ctx.obj["port"]
    ssl = ctx.obj["ssl"]
    ssl_ciphers = ctx.obj["ssl_ciphers"]
    connection_timeout = ctx.obj["connection_timeout"]
    logger.debug(f"imapbackup.do_upload_eml connect to IMAP server start...")
    server = get_imap_server(username, password, host, port, enable_ssl=ssl, ssl_ciphers=ssl_ciphers, timeout=connection_timeout)
    logger.debug(f"imapbackup.do_upload_eml connect to IMAP server success: server={server}...")
    mailbox = Mailbox(server)
    logger.debug(f"imapbackup.do_upload_eml search eml filenames...")
    eml_filenames = []
    for filename in data:
        filename = os.path.abspath(filename)
        if os.path.isfile(filename):
            eml_filenames.append(filename)
        elif os.path.isdir(filename):
            for root, dirs, files in os.walk(filename):
                for f in files:
                    if f.endswith(".eml"):
                        eml_filenames.append(os.path.join(root, f))
    logger.debug(f"imapbackup.do_upload_eml searched eml filenames: eml_filenames={eml_filenames}...")
    for eml_filename in eml_filenames:
        logger.debug(f"imapbackup.do_upload_eml uploading eml file: eml_filename={eml_filename}...")
        try:
            mailbox.upload_eml(folder, eml_filename)
            logger.debug(f"imapbackup.do_upload_eml uploading eml file success: eml_filename={eml_filename}...")
        except Exception as error:
            logger.debug(f"imapbackup.do_upload_eml uploading eml file failed: eml_filename={eml_filename}, error={error}...")

@main.command("restore")
@click.argument("backup_root", nargs=1, required=True)
@click.pass_context
def do_restore(ctx, backup_root):
    """Restore all backup email files to IMAP server.
    """
    logger.debug("imapbackup.do_restore start...")
    username = ctx.obj["username"]
    password = ctx.obj["password"]
    host = ctx.obj["host"]
    port = ctx.obj["port"]
    ssl = ctx.obj["ssl"]
    ssl_ciphers = ctx.obj["ssl_ciphers"]
    connection_timeout = ctx.obj["connection_timeout"]
    logger.debug(f"imapbackup.do_restore connect to IMAP server start...")
    server = get_imap_server(username, password, host, port, enable_ssl=ssl, ssl_ciphers=ssl_ciphers, timeout=connection_timeout)
    logger.debug(f"imapbackup.do_restore connect to IMAP server success: server={server}...")
    mailbox = Mailbox(server)
    table = []
    for folder in mailbox.get_all_folders():
        folder_name = folder[0]
        info = mailbox.restore(folder_name, backup_root)
        row = [folder_name]
        row += info
        table.append(row)
    print(tabulate(table, headers=["Folder", "Uploaded", "Failed", "New", "Total"]))

if __name__ == "__main__":
    main()


