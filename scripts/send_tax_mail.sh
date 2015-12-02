#!/bin/sh

FACEBOOK_CONSUMER_KEY=key
FACEBOOK_CONSUMER_SECRET=secret
export FACEBOOK_CONSUMER_KEY
export FACEBOOK_CONSUMER_SECRET


# Backup script for FRP, saves postgres and images to the cloud
VENV=/home/alokk/frp-env-new

# Activate virtualenv
. ${VENV}/bin/activate

python send_tax_mail.py mail
