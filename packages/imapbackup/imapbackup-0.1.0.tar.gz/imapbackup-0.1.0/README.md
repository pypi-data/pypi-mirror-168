# imapbackup

Download all emails from IMAP server, and save email to .eml files. And allow you restore these emails to a new imap server.

## Install

```
pip install imapbackup
```

## Usage

### main
```
test@test emailbackup % imapbackup
Usage: imapbackup [OPTIONS] COMMAND [ARGS]...

Options:
  --username TEXT                 IMAP account username.  [required]
  --password TEXT                 IMAP account password.  [required]
  --host TEXT                     IMAP server host.  [required]
  --port INTEGER                  IMAP server port, default to 993 if SSL is
                                  enabled and default to 143 if SSL is not
                                  enabled.
  --ssl / --no-ssl                Enable ssl.
  --ssl-ciphers TEXT              SSL ciphers used to make SSL connection.
  --connection-timeout INTEGER    Connection timeout.
  --loglevel [DEBUG|INFO|WARN|ERROR]
  --logfmt [default|simple|message_only]
  --help                          Show this message and exit.

Commands:
  backup   Backup folders from IMAP server.
  list     List all folders of the IMAP server.
  restore  Restore all backup email files to IMAP server.
  upload   Upload eml to IMAP server.

```

### backup

```
test@test emailbackup % imapbackup --host <imap.server.address> --ssl --username <username> --password <password> backup --help
Usage: imapbackup backup [OPTIONS] [FOLDER]...

  Backup folders from IMAP server. If no folder given, then backup all
  folders.

  Data save structure:

  ----------------------------------------------------------

  <Dest>

      <MailFolder 1>

          <mail_uid>-<mail_date>-<subject>-<mail_code>.eml

      <MailFolder ...>

          <mail_uid>-<mail_date>-<subject>-<mail_code>.eml

  ----------------------------------------------------------

  <Dest>: is your data storage root. Given by option -d.

  <MailFolder>: is the folder name from the IMAP server.

  <mail_uid>: is the mail's UID from the IMAP server.

  <mail_date>: is the mail's INTERNALDATE from the IMAP server.

  <subject>: is the mail's Subject. We replace slash “/” sign to underline "_"
  sign.

  <mail_code>: is the sha1 hash code of the mail's BODY.

  ----------------------------------------------------------

Options:
  -l, --limit INTEGER  Fetch limit.
  -d, --dest TEXT      Dest folder. Data storage root. Default to ./data/.
  --help               Show this message and exit.
```

### list

```
test@test emailbackup % imapbackup --host <imap.server.address> --ssl --username <username> --password <password> list --help  
Usage: imapbackup list [OPTIONS]

  List all folders of the IMAP server.

Options:
  --folder-name-max-length INTEGER
  --folder-name-mask TEXT
  --help                          Show this message and exit.
```

### restore

```
test@test emailbackup % imapbackup --host <imap.server.adddress> --ssl --username <username> --password <password> restore --help
Usage: imapbackup restore [OPTIONS] BACKUP_ROOT

  Restore all backup email files to IMAP server.

Options:
  --help  Show this message and exit.
```

### upload 

```
test@test emailbackup % imapbackup --host <imap.server.adddress> --ssl --username <username> --password <password> upload --help 
Usage: imapbackup upload [OPTIONS] DATA...

  Upload eml to IMAP server.

Options:
  -f, --folder TEXT  Upload eml to this folder. The folder MUST be created
                     already. Default to INBOX.
  --help             Show this message and exit.
```

## Example

1. backup imap server.

```
imapbackup --host <imap.server.address> --ssl --username username01@example.com --password 'Password!' --loglevel=DEBUG backup --dest 'username01@example.com'
```

1. Your IMAP server address is `<imap.server.address>`, and using ssl connection, so that the imap server port is 993.
1. Your email adddress is `username01@example.com` and your password is `Password!`.
1. Write process log to `logs/app.log`, and set the log level to DEBUG.
1. Save the backup emails under folder `username01@example.com`, group by IMAP folder, e.g. INBOX, 已发送.

1. restore the backup data.
```
imapbackup --host <imap.server.address> --ssl --username username01@example.com --password 'Password!' --loglevel=DEBUG restore 'username01@example.com'
```

1. Upload all emails under folder `username01@example.com` to the IMAP server.
1. Mostly the emails are created by `imapbackup` command.

## Release

### v0.1.0

- First release.
