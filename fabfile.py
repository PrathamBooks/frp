from fabric.api import run, cd, env, settings, sudo, local


env.hosts = ['ubuntu@ec2-54-251-215-76.ap-southeast-1.compute.amazonaws.com']
env.key_filename = ['/home/noufal/.ssh/id_rsa_pratham']


app_repository = "https://github.com/PrathamBooks/frp.git"

app_base = "/opt/frp"
deployments_dir = "{0}/deployments".format(app_base)
app_virtualenv = "frp-app"


def obtain_code(tag):
    with cd(deployments_dir):
        run("git clone -q {0} {1}".format(app_repository, tag))
        run("cd {0}/{1} && git checkout {1}".format(deployments_dir, tag))
        
def set_deployed_version(tag):
    with cd(app_base):
        run("rm -f deployed")
        run("ln -s {0}/{1} deployed".format(deployments_dir, tag))
    
def update_monit_config():
    sudo("ln -s {0}/scripts/monit/frp.conf /etc/monit/conf.d/frp.conf".format(app_base))

def push_code():
    local("git push --tags")

def deploy_app(tag):
    "Deploy the application tagged by :tag:"
    push_code()
    obtain_code(tag)
    set_deployed_version(tag)
    update_monit_config()

    
    


        
        

    
