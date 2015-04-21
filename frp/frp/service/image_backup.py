import boto
import gcs_oauth2_boto_plugin
import os
# URI scheme for Google Cloud Storage.
GOOGLE_STORAGE = 'gs'
# URI scheme for accessing local files.
LOCAL_FILE = 'file'

IMAGES_BUCKET = 'frp-production/images'
def save_image(directory, filename):
  print "In save image"
  errors = []
  try:
    with open(os.path.join(directory, filename), 'r') as localfile:
      print "opened file"
      dst_uri = boto.storage_uri(
        IMAGES_BUCKET + '/' + filename, GOOGLE_STORAGE)
    # The key-related functions are a consequence of boto's
    # interoperability with Amazon S3 (which employs the
    # concept of a key mapping to localfile).
      dst_uri.new_key().set_contents_from_file(localfile)
      print 'Successfully created "%s/%s"' % (
        dst_uri.bucket_name, dst_uri.object_name)
      return dst_uri.bucket_name + '/' + dst_uri.object_name
  except:
    errors.append('Unable to save image')
    return errors


