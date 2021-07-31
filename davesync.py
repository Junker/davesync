#!/usr/bin/python

import os
import sys
import argparse
import gnupg
import tempfile
import json
import colorlog
from pathlib import Path
from webdav4.client import Client
import webdav4


# ============================ FUNCS

def assert_on_bad_file(path):
	assert os.path.isfile(path) and os.access(path, os.R_OK), \
		"File {} doesn't exist or isn't readable".format(path)

def assert_on_bad_dir(path):
	assert os.path.isdir(path) and os.access(path, os.R_OK), \
		"Directory {} doesn't exist or isn't readable".format(path)

def assert_on_bad_webdav_dir(path):
	error_msg = "WebDav directory '{}' doesn't exist".format(remote_base + '/' + path)

	try:
		assert webdav.isdir(path), \
			error_msg
	except webdav4.client.ResourceNotFound:
		logger.critical(error_msg)
		sys.exit(1)


def encrypt_file(path):
	f = open(path, 'rb')

	fd, tempfilepath = tempfile.mkstemp()

	res = gpg.encrypt_file(f, None, symmetric=args.cipher_algo, passphrase=gpg_passphrase, output=tempfilepath,
						   extra_args=['--compress-algo', args.compress_algo,
									   '-z', args.compress_level,
									   '--set-filename', os.path.basename(path)])


	f.close()

	if not res:
		raise RuntimeError(f'GPG Error: {res.status}')

	return tempfilepath

def remove_str_suffix(text, suffix):
	if text is not None and suffix is not None:
		return text[:-len(suffix)] if text.endswith(suffix) else text
	else:
		return text

def read_webdav_password():
	if args.webdav_password_file:
		assert_on_bad_file(args.webdav_password_file)
		return Path(args.webdav_password_file).read_text().strip()
	else:
		return args.webdav_password

def read_gpg_passphrase():
	if args.gpg_passphrase_file:
		assert_on_bad_file(args.gpg_passphrase_file)
		return Path(args.gpg_passphrase_file).read_text().strip()
	else:
		return args.gpg_passphrase

def create_logger():
	logger = colorlog.getLogger(__file__) if args.verbose == 2 else colorlog.getLogger()
	logger.setLevel(colorlog.colorlog.logging.INFO)
	handler = colorlog.StreamHandler()
	handler.setFormatter(colorlog.ColoredFormatter("%(log_color)s %(message)s"))
	logger.addHandler(handler)

	if args.verbose > 1:
		logger.setLevel(colorlog.colorlog.logging.DEBUG)

	return logger

def parse_args():
	parser = argparse.ArgumentParser(description='sync and encrypt your local directory to WebDav server')
	parser.add_argument('local_base', type=str, help='Local directory to sync, e.g. /home/bob/myfolder')
	parser.add_argument('remote_base', type=str, help='Base WebDav URL, e.g. https://example.org/dav/myfolder')
	parser.add_argument('--webdav-user', '-u', type=str, help='WebDav Username')
	parser.add_argument('--webdav-password', '-p', type=str, help='WebDav Password')
	parser.add_argument('--webdav-password-file', type=str, help='WebDav Password file')
	parser.add_argument('--gpg-passphrase', '-gp', type=str, help='GPG Passphrase')
	parser.add_argument('--gpg-passphrase-file', type=str, help='GPG Passphrase file')
	parser.add_argument('--timeout', '-t', type=int, help='WebDav operation timeout. Default: %(default)s', default=10)
	parser.add_argument('--save-metadata-step', type=int, help='save metadata every N uploaded files. Default: %(default)s', default=10)
	parser.add_argument('--no-check-certificate', nargs='?', const=True, help='Do not verify SSL certificate')
	parser.add_argument('--cipher-algo', type=str, default='AES', help='Cipher algorithm. Default: %(default)s. (IDEA, 3DES, CAST5, BLOWFISH, AES, AES192, AES256, TWOFISH, CAMELLIA128, CAMELLIA192, CAMELLIA256 etc. Check your "gpg" command line help to see what symmetric cipher algorithms are supported)')
	parser.add_argument('--compress-algo', type=str, default='none', help='Compression algorithm. Default: %(default)s. (zip, zlib, bzip2, none etc. Check your "gpg" command line help to see what compression algorithms are supported)')
	parser.add_argument('--compress-level', '-z', type=str, default='0', help='Set compression level to N. Default: %(default)s')
	parser.add_argument('--verbose', '-v', action='count', help='verbose (-v,-vv,-vvv)', default=0)


	return parser.parse_args()

def load_metadata():
	logger.info('Loading metadata from remote dir...')

	if webdav.exists(METADATA_FILENAME):
		tmpfile = tempfile.TemporaryFile('wb+')
		webdav.download_fileobj(METADATA_FILENAME, tmpfile)
		tmpfile.seek(0)
		data = json.load(tmpfile)
		tmpfile.close()

		return data
	else:
		return {}

def upload_metadata(metadata):
	logger.info('Uploading metadata to remote dir...')

	tmpfile = tempfile.TemporaryFile('rb+')
	tmpfile.write(json.dumps(metadata).encode())
	tmpfile.seek(0)
	webdav.upload_fileobj(tmpfile, METADATA_FILENAME, overwrite=True)
	tmpfile.close()

# ============================ CODE

METADATA_FILENAME = 'davesync-metadata.json'

args = parse_args()
logger = create_logger()

local_base	= args.local_base.rstrip('/')
remote_base = args.remote_base.rstrip('/')

assert_on_bad_dir(local_base)

webdav_password = read_webdav_password()
gpg_passphrase = read_gpg_passphrase()

if (gpg_passphrase == None or not gpg_passphrase):
	logger.critical('GPG passphrase is not set')
	sys.exit(1)


gpg = gnupg.GPG()
webdav = Client(remote_base, auth=(args.webdav_user, webdav_password) if args.webdav_user != None else None, verify=not args.no_check_certificate, timeout=args.timeout)

assert_on_bad_webdav_dir('')

metadata = load_metadata()
new_metadata = {}

files_uploaded = 0

# traverse local base dir
logger.info('Checking files...')
for root, dirs, files in os.walk(local_base):
	assert_on_bad_dir(root)

	relpath = os.path.relpath(root, local_base)

	logger.debug(f"Checking Dir: '{root}'...")

	if relpath in ['/', '.']:
		relpath = ''

	if relpath != '':
		if webdav.exists(relpath):
			if (not webdav.isdir(relpath)):
				webdav.remove(relpath)
				webdav.mkdir(relpath)
		else:
			webdav.mkdir(relpath)

	dav_items = {item['name']:item for item in webdav.ls(relpath)}
	dav_files = dav_items.keys()

	for filename in files:

		dav_filename = filename + '.gpg'
		dav_filepath = (relpath + '/' + dav_filename).strip("/")
		full_filepath = os.path.join(root, filename)
		rel_filepath = os.path.join(relpath, filename)
		modified_time = os.path.getmtime(full_filepath)

		logger.debug(f"Checking file: '{rel_filepath}'...")

		new_metadata[dav_filepath] = {'modified': modified_time}

		# remove directory from webdav if it has same name as local file
		if dav_filepath in dav_files and dav_items[dav_filepath]['type'] != 'file':
			webdav.remove(dav_filepath)

		# upload file if it doesn't exist or modified
		if dav_filepath not in dav_files or (dav_filepath not in metadata) or (dav_filepath in metadata and metadata[dav_filepath]['modified'] != modified_time):
			logger.info(f"Uploading file '{dav_filepath}'...")

			try:
				tempfilepath = encrypt_file(full_filepath)
			except RuntimeError as err:
				logger.critical(err)
				sys.exit(1)


			webdav.upload_file(tempfilepath, dav_filepath, overwrite=True)
			os.unlink(tempfilepath)

			files_uploaded += 1

			# save metadata with modified timestamps of uploaded files
			if files_uploaded % args.save_metadata_step == 0:
				upload_metadata({**metadata, **new_metadata})


upload_metadata(new_metadata)


# traverse remote base dir
logger.info('Checking WebDav files...')
def webdav_scan_recursively(root_dir):

	items = webdav.ls(root_dir)

	for item in items:
		if item['name'] == METADATA_FILENAME:
			continue

		logger.debug("Checking WebDav %s '%s'", item['type'], item['name'])

		local_path = os.path.join(local_base, item['name'])

		if item['type'] == 'file':
			local_path = remove_str_suffix(local_path, '.gpg')

		if not os.path.exists(local_path):
			logger.info("Remove %s '%s' from WebDav", item['type'], item['name'])
			webdav.remove(item['name'])
		else:
			if item['type'] == 'directory':
				webdav_scan_recursively(item['name'])

webdav_scan_recursively('')
