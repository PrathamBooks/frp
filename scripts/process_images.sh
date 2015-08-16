
#!/bin/sh
# Backup script for FRP, saves postgres and images to the cloud
VENV=/home/alokk/frp-env-new

# Activate virtualenv
. ${VENV}/bin/activate

python process_images.py
