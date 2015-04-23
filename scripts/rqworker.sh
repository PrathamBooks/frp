#!/bin/sh

# Management script for rqworker managed by system monit. 

# If you change any of these file locations, please make corresponding
# changes in the /etc/monit/conf.d/frp.conf file on the server. The
# local file scripts/monit/rqworker.conf is what you should change and
# deploy if you want to do this.

VENV=/home/infodigital/frp-env
PID_FILE=/home/infodigital/frp/rqworker.pid
FACEBOOK_CONSUMER_KEY=key
FACEBOOK_CONSUMER_SECRET=secret
export FACEBOOK_CONSUMER_KEY
export FACEBOOK_CONSUMER_SECRET



# Activate virtualenv
. ${VENV}/bin/activate
case $1 in
   start)
      cd /home/infodigital/frp/frp; rqworker ;; 
   stop)
      kill `cat ${PID_FILE}` ;;
    *)  
      echo "usage: rqworker.sh {start|stop}" ;;
esac
exit 0
