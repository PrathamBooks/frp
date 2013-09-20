from fabric.api import run, cd, env, settings, sudo, local


env.hosts = ['ubuntu@ec2-54-251-215-76.ap-southeast-1.compute.amazonaws.com']
env.key_filename = ['/home/noufal/.ssh/id_rsa_pratham']


app_repository = "https://github.com/PrathamBooks/frp.git"

app_base = "/opt/frp"
deployments_dir = "{0}/deployments".format(app_base)
currently_deployed_dir = "{0}/deployed".format(app_base)

virtualenv_home = "/opt/frp/environments"
app_virtualenv = "frp-app"


def obtain_code(tag):
    with cd(deployments_dir):
        run("rm -Rf {0}".format(tag))
        run("git clone -q {0} {1}".format(app_repository, tag))
        run("cd {0}/{1} && git checkout {1}".format(deployments_dir, tag))
        
def set_deployed_version(tag):
    with cd(app_base):
        run("rm -f {0}".format(currently_deployed_dir))
        run("ln -s {0}/{1} {2}".format(deployments_dir, tag, currently_deployed_dir))
    
def update_monit_config():
    sudo("rm -f /etc/monit/conf.d/frp.conf")
    sudo("ln -s {0}/scripts/monit/frp.conf /etc/monit/conf.d/frp.conf".format(currently_deployed_dir))

def update_virtualenv(tag):
    with cd(app_base):
        run(". {0}/{1}/bin/activate && pip install -M -r {2}/requirements/production.txt".format(virtualenv_home, app_virtualenv, currently_deployed_dir))

def push_code():
    local("git push --tags")

def deploy_app(tag, venv = False):
    "Deploy the application tagged by :tag:"
    push_code()
    obtain_code(tag)
    set_deployed_version(tag)
    if venv:
        update_virtualenv(tag)
    update_monit_config()


    
    


        
        

    
