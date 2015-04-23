import boto
import gcs_oauth2_boto_plugin
import os
# URI scheme for Google Cloud Storage.
GOOGLE_STORAGE = 'gs'
# URI scheme for accessing local files.
LOCAL_FILE = 'file'

IMAGES_BUCKET = 'frp-production/images'
def save_image(directory, filename):
  with open("/home/infodigital/log/image_backup.log", "a") as log:
    log.write('Trying to save ' + directory + ' ' + filename + '\n')
    errors = []
    try:
      with open(os.path.join(directory, filename), 'r') as localfile:
        log.write('opened file ' + directory + ' ' + filename)
        dst_uri = boto.storage_uri(
          IMAGES_BUCKET + '/' + filename, GOOGLE_STORAGE)
        dst_uri.new_key().set_contents_from_file(localfile)
        log.write('Successfully created ' + dst_uri.bucket_name + ' ' + dst_uri.object_name + '\n')
    except:
      errors.append('Unable to save image')
      return errors


