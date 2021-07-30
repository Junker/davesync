# DavESync (WebDav Encrypted Synchronization)

Sync and encrypt your local directory to WebDav foldewr or your cloud with WebDav support (NextCloud, Yandex.Disk etc).

All files encrypted with GPG symmetric passphrase, you can download any file from your webdav or cloud and decrypt it with GPG app, which exists in any OS (Android, iOS, Linux, Windows etc).

## Usage 
```
davesync.py local_base remote_base [options]
Process some integers.

positional arguments:
  local_base            Local directory to sync, e.g. /home/bob/myfolder
  remote_base           Base WebDav URL, e.g. https://example.org/dav/myfolder

optional arguments:
  -h, --help            show this help message and exit
  --webdav-user WEBDAV_USER, -u WEBDAV_USER
                        Username
  --webdav-password WEBDAV_PASSWORD, -p WEBDAV_PASSWORD
                        WebDav Password
  --webdav-password-file WEBDAV_PASSWORD_FILE
                        WebDav Password file
  --gpg-passphrase GPG_PASSPHRASE, -gp GPG_PASSPHRASE
                        GPG Passphrase
  --gpg-passphrase-file GPG_PASSPHRASE_FILE
                        GPG Passphrase file
  --timeout TIMEOUT, -t TIMEOUT
                        WebDav operation timeout
  --save-metadata-step SAVE_METADATA_STEP
                        save metadata every N files
  --no-check-certificate [NO_CHECK_CERTIFICATE]
                        Do not verify SSL certificate
  --verbose, -v         verbose (-v,-vv,-vvv)
```

## Caveats:
- filenames not encrypted
