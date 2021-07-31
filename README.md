# DavESync (WebDav Encrypted Synchronization)

Sync and encrypt your local directory to WebDav folder or your cloud with WebDav support (NextCloud, Yandex.Disk etc).

All files are encrypted with GPG symmetric passphrase, you can download any file from your webdav or cloud and decrypt it with GPG app, which exists in any OS (Android, iOS, Linux, Windows etc).

## Requirements
- [webdav4](https://pypi.org/project/webdav4/)
- [python-gnupg](https://pypi.org/project/python-gnupg/)
- [colorlog](https://pypi.org/project/colorlog/)

## Usage 
```
davesync.py local_base remote_base [options]
sync and encrypt your local directory to WebDav server

positional arguments:
  local_base            Local directory to sync, e.g. /home/bob/myfolder
  remote_base           Base WebDav URL, e.g. https://example.org/dav/myfolder

optional arguments:
  -h, --help            show this help message and exit
  --webdav-user WEBDAV_USER, -u WEBDAV_USER
                        WebDav Username
  --webdav-password WEBDAV_PASSWORD, -p WEBDAV_PASSWORD
                        WebDav Password
  --webdav-password-file WEBDAV_PASSWORD_FILE
                        WebDav Password file
  --gpg-passphrase GPG_PASSPHRASE, -gp GPG_PASSPHRASE
                        GPG Passphrase
  --gpg-passphrase-file GPG_PASSPHRASE_FILE
                        GPG Passphrase file
  --delete [DELETE]     delete extraneous files/dirs from remote dirs.
  --timeout TIMEOUT, -t TIMEOUT
                        WebDav operation timeout. Default: 10
  --save-metadata-step SAVE_METADATA_STEP
                        save metadata every N uploaded files. Default: 10
  --no-check-certificate [NO_CHECK_CERTIFICATE]
                        Do not verify SSL certificate
  --cipher-algo CIPHER_ALGO
                        Cipher algorithm. Default: AES. (IDEA, 3DES, CAST5, BLOWFISH, AES, AES192, AES256, TWOFISH, CAMELLIA128, CAMELLIA192, CAMELLIA256 etc. Check your "gpg" command line help to see what symmetric cipher algorithms are supported)
  --compress-algo COMPRESS_ALGO
                        Compression algorithm. Default: none. (zip, zlib, bzip2, none etc. Check your "gpg" command line help to see what compression algorithms are supported)
  --compress-level COMPRESS_LEVEL, -z COMPRESS_LEVEL
                        Set compression level to N. Default: 0
  --verbose, -v         verbose (-v,-vv,-vvv)

```

## Caveats:
- filenames not encrypted
