#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement

import os
import re
import json
import time
import email
import imaplib
import logging

from imapclient import imap_utf7
from dateutil.parser import parse as parse_datetime
from zenutils import hashutils
from zenutils import fsutils
from zenutils import strutils

logger = logging.getLogger(__name__)

class Mailbox(object):
    imap_list_expected = "OK"
    imap_select_expected = "OK"
    imap_search_expected = "OK"
    imap_fetch_expected = "OK"
    imap_append_expected = "OK"
    save_filename_template = "{mail_uid}-{mail_datetime}-{mail_subject}-{mail_body_hashcode}.eml"
    save_filename_pattern = "(?P<mail_uid>\d+)-(?P<mail_datetime>\d+)-(?P<mail_subject>.*)-(?P<mail_subject_hashcode>[0-9a-f]*).eml"
    no_subject_title = "无标题"

    def __init__(self, imap_instance):
        self.imap_instance = imap_instance
        self.folder = None

    @classmethod
    def get_mail_info_from_eml_filename(cls, eml_filename):
        logger.debug(f"Mailbox.get_mail_info_from_eml_filename start: save_filename_pattern={cls.save_filename_pattern}, eml_filename={eml_filename}...")
        try:
            info = re.match(cls.save_filename_pattern, eml_filename).groupdict()
            logger.debug(f"Mailbox.get_mail_info_from_eml_filename success: save_filename_pattern={cls.save_filename_pattern}, eml_filename={eml_filename}, info={info}...")
            return info
        except Exception as error:
            logger.warning(f"Mailbox.get_mail_info_from_eml_filename success: save_filename_pattern={cls.save_filename_pattern}, eml_filename={eml_filename}, error={error}...")
            return None

    @classmethod
    def get_mail_subject(cls, mail):
        """Get mail's subject from the email instance.
        """
        logger.debug(f"Mailbox.get_mail_subject start...")
        raw_subject = mail.get("Subject")
        logger.debug(f"Mailbox.get_mail_subject get raw subject from the email instance success: raw_subject={raw_subject}...")
        if raw_subject is None:
            logger.warning(f"Mailbox.get_mail_subject get NO subject from the email instance, mail={mail}...")
            return cls.no_subject_title
        try:
            subject_info = email.header.decode_header(raw_subject)
            final_subject = ""
            for title, encoding in subject_info:
                if encoding:
                    try:
                        title = title.decode(encoding)
                    except Exception:
                        pass
                final_subject += " " + strutils.force_text(title)
            logger.debug(f"Mailbox.get_mail_subject success: raw_subject={raw_subject}, subject={final_subject}...")
            return final_subject
        except Exception as error:
            logger.exception(f"Mailbox.get_mail_subject failed: raw_subject={raw_subject}, error={error}...")
            raise error

    @classmethod
    def get_folder_name(cls, name):
        """Parse imap_utf7 encoded folder name string, and returns it's orginal plain name.

        @Example:
            get_folder_name('"&XfJT0ZAB-"') returns "已发送"

        """
        logger.debug(f"Mailbox.get_folder_name start: name={name}...")
        decoded_name = imap_utf7.decode(name)
        if decoded_name.startswith('"'):
            decoded_name = decoded_name[1:]
        if decoded_name.endswith('"'):
            decoded_name = decoded_name[:-1]
        logger.debug(f"Mailbox.get_folder_name success: name={name}, decoded_name={decoded_name}...")
        return decoded_name

    @classmethod
    def load_backup_uids(cls, root, folder):
        """Load uids from backup storage.
        """
        logger.debug(f"Mailbox.load_backup_uids start: root={root}, folder={folder}...")
        mail_uids = set()
        path = os.path.join(root, folder)
        if not os.path.exists(path): # folder not exists, returns empty set
            return mail_uids
        eml_filenames = [x for x in os.listdir(path) if x.endswith(".eml")] # find all .eml filenames
        for filename in eml_filenames:
            info = cls.get_mail_info_from_eml_filename(filename)
            if not info:
                continue
            if not "mail_uid" in info:
                continue
            mail_uids.add(info["mail_uid"])
        logger.debug(f"mailbox.load_backup_uids success: mail_uids={mail_uids}...")
        return mail_uids

    def get_all_folders(self):
        """Get all folder names from IMAP server.

        @Returns: List[(<name>, <path>)]

        @Returns-Example:
            INBOX    ()
            草稿箱   (\Drafts)
            已发送   (\Sent)
            已删除   (\Trash)
            垃圾邮件 (\Junk)
            通知类   ()
            重要通知 ()
        """
        logger.debug(f"Mailbox.get_all_folders start:  imap_instance={self.imap_instance}...")
        folders = []
        status, data = self.imap_instance.list()
        if status != self.imap_list_expected:
            msg = f"Mailbox.get_all_folders do self.imap_instance.list failed: imap_instance={self.imap_instance}, status={status}, data={data}..."
            logger.error(msg)
            raise Exception(msg)
        for line in data:
            path, name = line.split(b' "/" ')
            path = path.decode()
            name = self.get_folder_name(name)
            folders.append((name, path))
        logger.debug(f"Mailbox.get_all_folders start:  imap_instance={self.imap_instance}, folder={folders}...")
        return folders

    def select_folder(self, folder="INBOX"):
        """IMAP Instance do select a folder.

        @Parameter: folder
            Raw plain text folder name. Default to INBOX.

        @Returns: true
            Always returns true if select folder success. Exception will be raised if select folder failed.

        """
        msg = f"Mailbox.select_folder start: folder={folder}..."
        logger.debug(msg)
        status, data = self.imap_instance.select(imap_utf7.encode(folder))
        if status != self.imap_select_expected:
            msg = f"Mailbox.select_folder failed: imap_instance={self.imap_instance}, folder={folder}, status={status}, data={data}..."
            logger.error(msg)
            raise Exception(msg)
        else:
            msg = f"Mailbox.select_folder success: imap_instance={self.imap_instance}, folder={folder}, status={status}, data={data}..."
            logger.debug(msg)
        self.folder = folder # keep current folder
        return True

    def get_mail_uids(self, folder):
        """Get mail uid set from IMAP server.

        @Returns:
            set

        @Returns Example:
            {
                "38281",
                "38282",
                ...
            }
        """
        logger.debug(f"Mailbox.get_mail_uids start: imap_instance={self.imap_instance}, folder={self.folder}...")
        if self.folder != folder:
            assert self.select_folder(folder)
        status, data = self.imap_instance.search(None, "ALL")
        if status != self.imap_search_expected:
            msg = f"Mailbox.get_mail_uids search the folder failed: imap_instance={self.imap_instance}, folder={folder}, status={status}, data={data}..."
            logger.error(msg)
            raise Exception(msg)
        else:
            msg = f"Mailbox.get_mail_uids search the folder success: imap_instance={self.imap_instance}, folder={folder}, status={status}, data={data}..."
            logger.debug(msg)
        try:
            mailids = [x.decode() for x in data[0].split()]
            msg = f"Mailbox.get_mail_uids parse mailids success: imap_instance={self.imap_instance}, folder={folder}, status={status}, data={data}, mailids={mailids}..."
            logger.debug(msg)
        except Exception as error:
            msg = f"Mailbox.get_mail_uids parse mailids failed: imap_instance={self.imap_instance}, folder={folder}, status={status}, data={data}, error={error}..."
            logger.error(msg)
            raise Exception(msg)
        if not mailids: # empty folder
            return set()
        status, data = self.imap_instance.fetch(",".join(mailids), "UID")
        if status != self.imap_fetch_expected:
            msg = f"Mailbox.get_mail_uids fetch mail uids failed: imap_instance={self.imap_instance}, folder={folder}, status={status}, data={data}..."
            logger.error(msg)
            raise Exception(msg)
        else:
            msg = f"Mailbox.get_mail_uids fetch mail uids success: imap_instance={self.imap_instance}, folder={folder}, status={status}, data={data}..."
            logger.debug(msg)
        mail_uids = set()
        try:
            lines = [x.decode() for x in data]
            for line in lines:
                info = re.findall("(\d+) \\(UID (\d+)\\)", line)
                if info:
                    uid = info[0][1]
                    mail_uids.add(uid)
            msg = f"Mailbox.get_mail_uids parse mail uids success: imap_instance={self.imap_instance}, folder={folder}, mail_uids={mail_uids}..."
            logger.debug(msg)
        except Exception as error:
            msg = f"Mailbox.get_mail_uids parse mail uids failed: imap_instance={self.imap_instance}, folder={folder}, status={status}, data={data}, error={error}..."
            logger.error(msg)
            raise Exception(msg)
        return mail_uids

    def backup(self, root, folder, limit=0):
        """Backup a IMAP server folder.

        @Returns: <downloaded_counter> <bad_counter> <new_counter> <total>

        """
        msg = f"Mailbox.backup start: root={root}, folder={folder}, limit={limit}..."
        logger.debug(msg)
        if self.folder != folder:
            assert self.select_folder(folder)
        downloaded_uids = self.load_backup_uids(root, folder)
        server_uids = self.get_mail_uids(folder)
        new_uids = server_uids - downloaded_uids
        msg = f"Mailbox.backup compare local and remote uids success: new_uids={new_uids}..."
        logger.debug(msg)
        if not new_uids:
            msg = f"Mailbox.backup compare local and remote uids success, and found there's NO new emails: downloaded_uids={downloaded_uids}, server_uids={server_uids}..."
            logger.info(msg)
        new_uids = list(new_uids)
        new_uids.sort(key=lambda x: int(x), reverse=True)
        bad_uids = []
        new_uids_total = len(new_uids)
        counter = 0
        downloaded_counter = 0
        for mail_uid in new_uids:
            counter += 1
            print(f"Mailbox.backup downloading email [{folder}-{mail_uid}] ({counter}/{new_uids_total})...")
            if limit and counter > limit:
                msg = f"Mailbox.backup got download limit: limit={limit}..."
                break
            try:
                self.download(mail_uid, folder, root=root)
                downloaded_counter += 1
            except Exception as error:
                msg = f"Mailbox.backup download email failed: mail_uid={mail_uid}, error={error}..."
                logger.warning(msg)
                bad_uids.append(mail_uid)
        return downloaded_counter, len(bad_uids), len(new_uids), len(server_uids)

    def download(self, mail_uid, folder, root):
        """Fetch the mail content of the given mail_uid, and save it to the folder under the root.
        """
        msg = f"Mailbox.download start: mail_uid={mail_uid}, folder={folder}, root={root}..."
        logger.debug(msg)
        if self.folder != folder:
            assert self.select_folder(folder)
        msg = f"Mailbox.download doing self.imap_instance.fetch start: mail_uid={mail_uid}, message_parts=(UID INTERNALDATE RFC822)..."
        logger.debug(msg)
        status, data = self.imap_instance.uid("FETCH", mail_uid, "(UID INTERNALDATE RFC822)")
        if status != self.imap_fetch_expected or (not data) or (data[0] is None):
            msg = f"Mailbox.download fetch mail info failed: imap_instance={self.imap_instance}, folder={folder}, root={root}, mail_uid={mail_uid}, status={status}, data={data}..."
            logger.error(msg)
            raise Exception(msg)
        else:
            msg = f"Mailbox.download fetch mail info success: imap_instance={self.imap_instance}, folder={folder}, root={root}, mail_uid={mail_uid}, status={status}, data={data}..."
            logger.debug(msg)
        # parse mail info
        try:
            result = re.findall(b"""(\d)+ \\(UID (\d+) INTERNALDATE \\"([^\\"]+)\\" RFC822 {\d+}""", data[0][0])
            mailid_new, mail_uid, mail_datetime = result[0]
            mailid_new = mailid_new.decode()
            mail_uid = mail_uid.decode()
            mail_datetime = parse_datetime(mail_datetime)
            mail_body = data[0][1]
            mail_body_hashcode = hashutils.get_sha1_hexdigest(mail_body)
            mail = email.message_from_bytes(mail_body)
            mail_subject = self.get_mail_subject(mail)
            save_filename = os.path.join(root, folder, fsutils.get_safe_filename(self.save_filename_template.format(
                mail_uid=mail_uid,
                mail_datetime=mail_datetime.strftime("%Y%m%d%H%M%S"),
                mail_subject=mail_subject,
                mail_body_hashcode=mail_body_hashcode,
            )))
            msg = f"Mailbox.download parse mail info success: imap_instance={self.imap_instance}, folder={folder}, root={root}, mail_uid={mail_uid}, mailid_new={mailid_new}, mail_uid={mail_uid}, mail_datetime={mail_datetime}, mail_subject={mail_subject}, save_filename={save_filename}..."
            logger.debug(msg)
        except Exception as error:
            msg = f"Mailbox.download parse mail info failed: imap_instance={self.imap_instance}, folder={folder}, root={root}, mail_uid={mail_uid}, status={status}, data={data}, error={error}..."
            logger.error(msg)
            raise Exception(msg)
        # save mail content
        fsutils.safe_write(save_filename, mail_body)

    def upload_eml(self, folder, eml_filename):
        """Upload eml file content to IMAP server.
        """
        msg = f"Mailbox.upload_eml start: imap_instance={self.imap_instance}, folder={folder}, eml_filename={eml_filename}..."
        logger.debug(msg)
        folder_encoded = imap_utf7.encode(folder)
        try:
            eml_data = fsutils.readfile(eml_filename, binary=True)
        except Exception as error:
            msg = f"Mailbox.upload_eml read eml content failed: imap_instance={self.imap_instance}, folder={folder}, eml_filename={eml_filename}, error={error}..."
            raise Exception(msg)
        status, data = self.imap_instance.append(folder_encoded, "", imaplib.Time2Internaldate(time.time()), eml_data)
        if status != self.imap_append_expected:
            msg = f"Mailbox.upload_eml failed: imap_instance={self.imap_instance}, folder={folder}, eml_filename={eml_filename}, status={status}, data={data}..."
            logger.error(msg)
            raise Exception(msg)
        else:
            msg = f"Mailbox.upload_eml success: imap_instance={self.imap_instance}, folder={folder}, eml_filename={eml_filename}, status={status}, data={data}..."
            logger.debug(msg)
        return True

    def restore(self, folder, root, uploaded_mail_uids_filename=".uploaded_mail_uids.json"):
        """Upload local .eml files to IMAP server.

        @Returns: <uploaded_counter> <bad_counter> <new_counter> <total>
            uploaded_counter: successfully uploaded counter in current process.
            bad_counter: upload failed counter in current process.
            new_counter: this process should uploaded counter.
            total: scaned emls.
        """
        logger.debug(f"Mailbox.restore start: root={root}, folder={folder}, uploaded_mail_uids_filename={uploaded_mail_uids_filename}...")
        folder_path = os.path.abspath(os.path.join(root, folder))
        if not os.path.exists(folder_path): # folder not exists
            msg = f"Mailbox.restore failed for eml folder not exists: root={root}, folder={folder}, folder_path={folder_path}..."
            logger.warning(msg)
            return 0, 0, 0, 0
        try:
            uploaded_mail_uids_file = os.path.join(folder_path, uploaded_mail_uids_filename)
            logger.debug(f"Mailbox.restore loading uploaded_mail_uids from file: {uploaded_mail_uids_file}...")
            uploaded_mail_uids_file_content = fsutils.readfile(uploaded_mail_uids_file, default="[]")
            logger.debug(f"Mailbox.restore loading uploaded_mail_uids from file got content: {uploaded_mail_uids_file_content}...")
            uploaded_mail_uids = json.loads(uploaded_mail_uids_file_content)
            uploaded_mail_uids = set(uploaded_mail_uids)
            logger.debug(f"Mailbox.restore loading uploaded_mail_uids from file got result: {uploaded_mail_uids}...")
        except Exception as error:
            msg = f"Mailbox.restore loading uploaded_mail_uids failed: root={root}, folder={folder}, uploaded_mail_uids_file={uploaded_mail_uids_file}, error={error}..."
            raise Exception(msg)
        try:
            eml_filenames = [x for x in os.listdir(folder_path) if x.endswith(".eml")]
            msg = f"Mailbox.restore scan eml folder got eml filenames: {eml_filenames}..."
            logger.debug(msg)
        except Exception as error:
            msg = f"Mailbox.restore scan eml folder failed: root={root}, folder={folder}, folder_path={folder_path}, error={error}..."
            logger.error(msg)
            raise Exception(msg)
        total = 0
        uploaded_counter = 0
        bad_counter = 0
        new_counter = 0
        for eml_filename in eml_filenames:
            info = self.get_mail_info_from_eml_filename(eml_filename)
            if not info:
                msg = f"Mailbox.restore doing get_mail_info_from_eml_filename failed: root={root}, folder={folder}, uploaded_mail_uids_filename={uploaded_mail_uids_filename}, eml_filename={eml_filename}..."
                logger.info(msg)
                continue
            total += 1
            mail_uid = info["mail_uid"]
            if mail_uid in uploaded_mail_uids:
                continue
            new_counter += 1
            eml_filename = os.path.join(folder_path, eml_filename)
            try:
                self.upload_eml(folder, eml_filename)
                uploaded_mail_uids.add(mail_uid)
                uploaded_counter += 1
            except Exception as error:
                msg = f"Mailbox.restore upload_eml failed: root={root}, folder={folder}, uploaded_mail_uids_filename={uploaded_mail_uids_filename}, eml_filename={eml_filename}, eml_info={info}..."
                logger.warning(msg)
                bad_counter += 1
        try:
            fsutils.safe_write(uploaded_mail_uids_file, json.dumps(list(uploaded_mail_uids)))
        except Exception as error:
            msg = f"Mailbox.restore save uploaded_mail_uids failed: Mailbox.restore start: root={root}, folder={folder}, uploaded_mail_uids_filename={uploaded_mail_uids_filename}, uploaded_mail_uids_file={uploaded_mail_uids_file}, uploaded_mail_uids={uploaded_mail_uids}..."
            logger.error(msg)
        return uploaded_counter, bad_counter, new_counter, total
