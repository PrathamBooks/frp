import re
import datetime
import time
import boto
import gcs_oauth2_boto_plugin
from subprocess import call

# URI scheme for Google Cloud Storage.
GOOGLE_STORAGE = 'gs'
# URI scheme for accessing local files.
LOCAL_FILE = 'file'

project_id = 'emerald-surface-650'

PSQL_BUCKET = 'frp-production/psql'

uri = boto.storage_uri(PSQL_BUCKET, GOOGLE_STORAGE)
# If for some reason backups are not happening, keep at least the old backups
count = 0
for obj in uri.get_bucket():
  count += 1

if (count < 20):
  print "Number of backups less than 20, sending mail"
  call('echo Problem in DAB backups | sendmail kuchlous@gmail.com', shell=True)
  exit

date = datetime.date(2015, 1, 1)

today = date.today()

for obj in uri.get_bucket():
  if (re.match('psql/postgres.*', obj.name)):
    m = re.match(r'(\d\d\d\d)-(\d\d)-(\d\d)', obj.last_modified)
    year = int(m.group(1))
    month = int(m.group(2))
    day = int(m.group(3))
    modified_date = datetime.date(year, month, day)
    if (today - modified_date >= datetime.timedelta(2)):
      print "Deleting " + obj.name
      obj.delete()
