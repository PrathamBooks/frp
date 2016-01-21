#!/bin/sh

# Backup script for FRP, saves postgres and images to the cloud
VENV=/home/infodigital/frp-env

# Activate virtualenv
. ${VENV}/bin/activate

python backup_db.py
python backup_tax_receipts.py
