#!/bin/bash
BASE_TOOLS_STATUS="/tmp/.vagrant-base_tools"
POSTGRESQL_CONFIG_STATUS="/tmp/.vagrant-postgresconfig"
VENV_CONFIG_STATUS="/tmp/.vagrant-venv"
PIP_INSTALL_STATUS="/tmp/.vagrant-pip-install"
CLONE="/tmp/.vagrant-clone"
BASHRC_UPDATE="/tmp/.vagrant-bashrc"
DATABASE_SYNC="/tmp/.vagrant-dbsync"

USER=$(whoami)

# # Install base tools
if [ ! -e ${BASE_TOOLS_STATUS} ]; then
    sudo apt-get update && 
    sudo apt-get -y install virtualenvwrapper postgresql rabbitmq-server git postgresql-server-dev-9.1 python-dev realpath &&
    touch ${BASE_TOOLS_STATUS}
fi

# # Configure postgreSQL
if [ ! -e ${POSTGRESQL_CONFIG_STATUS} ];then
    sudo -u postgres psql -c "CREATE USER vagrant WITH NOCREATEDB NOCREATEUSER ENCRYPTED PASSWORD E'vagrant' " &&
    sudo -u postgres psql -c "CREATE DATABASE agiliq_fundraiser WITH OWNER vagrant" &&
    touch ${POSTGRESQL_CONFIG_STATUS}
fi

if [ ${USER} = "root" ] ; then
    echo "Running rest of script as vagrant"
    exec sudo -u vagrant /bin/bash  /vagrant/agiliq-fundraiser.sh
fi

export WORKON_HOME=/home/vagrant/.virtualenvs/
# Load up virtualenvwrapper
. /etc/bash_completion.d/virtualenvwrapper

# Now create one for agiliqs-fundraiser
if [ ! -e ${VENV_CONFIG_STATUS} ]; then
    rmvirtualenv agiliq_fundraiser &&
    mkvirtualenv agiliq_fundraiser &&
    touch ${VENV_CONFIG_STATUS}
else
    workon agiliq_fundraiser
fi

# First install everything we need. 
if [ ! -e ${PIP_INSTALL_STATUS} ];then
    cd /tmp/ && 
    wget https://www.dropbox.com/s/a00hdlerdnz07gd/agiliq-fundraiser.pybundle &&
    pip install /tmp/agiliq-fundraiser.pybundle &&
    touch ${PIP_INSTALL_STATUS}
fi

# Now get the application from github
if [ ! -e ${CLONE} ]; then
    cd /home/vagrant/ &&
    rm -Rf fundraiser &&
    git clone https://github.com/nibrahim/fundraiser &&
    touch ${CLONE}
fi

# Now put our customisations into the vagrant users init file
if [ ! -e ${BASHRC_UPDATE} ];then
cat <<EOF >> /home/vagrant/.bashrc


# This is added to make virtualenvwrapper run properly
export WORKON_HOME="/home/vagrant/.virtualenvs/"
. /etc/bash_completion.d/virtualenvwrapper


# The following variables are automatically added by 
# the vagrant provisioner to get the agiliq fundraiser
# application to start.
export DB_NAME="agiliq_fundraiser"
export DB_USER="vagrant"
export DB_PASSWORD="vagrant"
# These need to be set somewhere
export EMAIL_HOST_USER=""
export EMAIL_HOST_PASSWORD=""
export MERCHANT_API_KEY=""
export MERCHANT_PUBLISHABLE_KEY=""
export EBS_ACCOUNT_ID=""
export EBS_SECRET_KEY=""
EOF

touch  ${BASHRC_UPDATE}
fi
 
# Also set them right now so that we can create and setup the database
export DB_NAME="agiliq_fundraiser"
export DB_USER="vagrant"
export DB_PASSWORD="vagrant"
export EMAIL_HOST_USER=""
export EMAIL_HOST_PASSWORD=""
export MERCHANT_API_KEY=""
export MERCHANT_PUBLISHABLE_KEY=""
export EBS_ACCOUNT_ID=""
export EBS_SECRET_KEY=""



# Get the database ready
if [ ! -e ${DATABASE_SYNC} ]; then
    cd /home/vagrant/fundraiser
    python manage.py syncdb  &&  
    python manage.py migrate &&
    touch ${DATABASE_SYNC}
fi


