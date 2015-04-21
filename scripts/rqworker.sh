#!/bin/sh

# Management script for rqworker managed by system monit. 

# If you change any of these file locations, please make corresponding
# changes in the /etc/monit/conf.d/frp.conf file on the server. The
# local file scripts/monit/rqworker.conf is what you should change and
# deploy if you want to do this.

VENV=/home/infodigital/frp-env
PID_FILE=/home/infodigital/frp/rqworker.pid


# Activate virtualenv
. ${VENV}/bin/activate
case $1 in
   start)
      python /home/infodigital/frp/scripts/rqworker.py ;; 
   stop)
      kill `cat ${PID_FILE}` ;;
    *)  
      echo "usage: rqworker.sh {start|stop}" ;;
esac
exit 0
