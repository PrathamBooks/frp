#!/bin/sh

# Management script for FRP application Managed by system monit. 

# If you change any of these file locations, please make corresponding
# changes in the /etc/monit/conf.d/frp.conf file on the server. The
# local file scripts/monit/frp.conf is what you should change and
# deploy if you want to do this.

VENV=/opt/frp/environments/frp-app
APP_ROOT=/opt/frp/deployed
PID_FILE=/opt/frp/frp.pid

# Activate virtualenv
. ${VENV}/bin/activate

case $1 in
   start)
      gunicorn --chdir ${APP_ROOT}/frp \
	  -D \
	  -p ${PID_FILE} \
	  --log-syslog \
	  --log-syslog-prefix=frp \
	  --log-syslog-facility=local0 \
	  --log-level=debug \
	  wsgi:app
      ;;
    stop)  
      kill `cat ${PID_FILE}` ;;
    *)  
      echo "usage: app.sh {start|stop}" ;;
esac
exit 0
