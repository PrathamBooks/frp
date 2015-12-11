import time
from subprocess import call
import boto
import gcs_oauth2_boto_plugin
import os
import shutil
import StringIO
import tempfile

RECEIPTS_DIR = "/home/infodigital/tax-receipts"
# URI scheme for Google Cloud Storage.
GOOGLE_STORAGE = 'gs'
# URI scheme for accessing local files.
LOCAL_FILE = 'file'

project_id = 'emerald-surface-650'

RECEIPTS_BUCKET = 'frp-production/tax-receipts'

for filename in os.listdir(RECEIPTS_DIR):
  with open(os.path.join(RECEIPTS_DIR, filename), 'r') as localfile:
    dst_uri = boto.storage_uri(
         RECEIPTS_BUCKET + '/' + filename, GOOGLE_STORAGE)
    # The key-related functions are a consequence of boto's
    # interoperability with Amazon S3 (which employs the
    # concept of a key mapping to localfile).
    dst_uri.new_key().set_contents_from_file(localfile)
    print 'Successfully created "%s/%s"' % (
       dst_uri.bucket_name, dst_uri.object_name)
    call(["rm","-f",RECEIPTS_DIR + "/" + filename])

