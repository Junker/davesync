# DavESync (WebDav Encrypted Synchronization)

Sync and encrypt your local directory to WebDav folder or your cloud with WebDav
support (NextCloud, Yandex.Disk etc).

All files are encrypted with GPG symmetric passphrase, you can download any file
from your webdav or cloud and decrypt it with GPG app, which exists in any OS
(Android, iOS, Linux, Windows etc).

## Dependencies

- [webdav4](https://pypi.org/project/webdav4/)
- [python-gnupg](https://pypi.org/project/python-gnupg/)
- [colorlog](https://pypi.org/project/colorlog/)

```shell
pip install -r requirements.txt
```

## Result example

Local folder:
```
/home/bob/mydata
│
├─bank_records.xlsx
├─my_nude_photo.jpg
├─very_secret_document.docx
└─passport.pdf
```

WebDav folder:
```
https://nextcloud.example.org/remote.php/dav/files/bob/mydata
│
├─bank_records.xlsx.gpg
├─my_nude_photo.jpg.gpg
├─very_secret_document.docx.gpg
├─passport.pdf.gpg
└─davesync-metadata.json
```

## Usage

e.g.:

```bash
$ davesync.py /home/bob/mydata https://nextcloud.example.org/remote.php/dav/files/bob/mydata \
    --webdav-user=bob \
    --webdav-password 123 \
    --gpg-passphrase qwe \
    --delete \
    --verbose
```

```
davesync.py local_base remote_base [options]
sync and encrypt your local directory to WebDav server

positional arguments:
  local_base            Local directory to sync, e.g. /home/bob/myfolder
  remote_base           Base WebDav URL, e.g. https://example.org/dav/myfolder

optional arguments:
  -h, --help            show this help message and exit
  --webdav-user USER, -u USER
                        WebDav Username
  --webdav-password PASSWORD, -p PASSWORD
                        WebDav Password
  --webdav-password-file PASSWORD_FILE
                        WebDav Password file
  --gpg-passphrase PASSPHRASE, -gp PASSPHRASE
                        GPG Passphrase
  --gpg-passphrase-file PASSPHRASE_FILE
                        GPG Passphrase file
  --delete              delete extraneous files/dirs from remote dirs.
  --delete-excluded     Delete excluded files from dest dirs
  --force, -f           Force copying of files. Do not check files modifications
  --timeout N, -t N     WebDav operation timeout N seconds. Default: 10
  --exclude PATTERN     exclude files matching PATTERN
  --save-metadata-step N
                        save metadata every N uploaded files. Default: 10
  --no-check-certificate
                        Do not verify SSL certificate
  --cipher-algo CIPHER  Cipher algorithm. Default: AES. (IDEA, 3DES, CAST5,
                        BLOWFISH, AES, AES192, AES256, TWOFISH, CAMELLIA128,
                        CAMELLIA192, CAMELLIA256 etc.
                        Check your "gpg" command line help to see what symmetric
                        cipher algorithms are supported)
  --compress-algo ALGO  Compression algorithm. Default: none.
                        (zip, zlib, bzip2, none etc. Check your "gpg" command
                         line help to see what compression algorithms are supported)
  --compress-level N, -z N
                        Set compression level to N. Default: 0
  --verbose, -v         verbose (-v,-vv,-vvv)

```

## Decrypt

### CLI

```bash
gpg example.docx.gpg
```

### GUI

Windows:

- [WinGPG](https://scand.com/products/wingpg/)

OSX:

- [GPGTools](https://gpgtools.org/)

Android:

- [OpenKeychain: Easy PGP](https://play.google.com/store/apps/details?id=org.sufficientlysecure.keychain)

## Caveats

- filenames not encrypted
