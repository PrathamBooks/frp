import time
from subprocess import call
import boto
import gcs_oauth2_boto_plugin
import os
import shutil
import StringIO
import tempfile

# URI scheme for Google Cloud Storage.
GOOGLE_STORAGE = 'gs'
# URI scheme for accessing local files.
LOCAL_FILE = 'file'

project_id = 'emerald-surface-650'

PSQL_BUCKET = 'frp-production/psql'

call(["rm","-f","postgres.dump"])
call(["ls","-l"])
now = time.time()
filename = 'postgres-%d.dump' % now
pg_dump_cmd = 'pg_dumpall > ' + filename 
call(pg_dump_cmd, shell=True)
with open(os.path.join('.', filename), 'r') as localfile:
  dst_uri = boto.storage_uri(
        PSQL_BUCKET + '/' + filename, GOOGLE_STORAGE)
    # The key-related functions are a consequence of boto's
    # interoperability with Amazon S3 (which employs the
    # concept of a key mapping to localfile).
  dst_uri.new_key().set_contents_from_file(localfile)
  print 'Successfully created "%s/%s"' % (
      dst_uri.bucket_name, dst_uri.object_name)

pg_cleanup_cmd = 'rm -f ' + filename
call(pg_cleanup_cmd, shell=True)
