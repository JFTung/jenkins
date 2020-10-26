# NOTE: Only necessary if using Jenkins workers/nodes/agents

import jenkins
import os
import signal
import sys
import urllib
import subprocess
import shutil
import requests
import time

worker_jar = '/var/lib/jenkins/worker.jar'
worker_name = os.environ['WORKER_NAME'] if os.environ['WORKER_NAME'] != '' else 'docker-worker-' + os.environ['HOSTNAME']
jnlp_url = os.environ['JENKINS_URL'] + '/computer/' + worker_name + '/worker-agent.jnlp'
worker_jar_url = os.environ['JENKINS_URL'] + '/jnlpJars/worker.jar'
print(worker_jar_url)
process = None

def clean_dir(dir):
    for root, dirs, files in os.walk(dir):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

def worker_create(node_name, working_dir, executors, labels):
    j = jenkins.Jenkins(os.environ['JENKINS_URL'], os.environ['JENKINS_USER'], os.environ['JENKINS_PASS'])
    j.node_create(node_name, working_dir, num_executors = int(executors), labels = labels, launcher = jenkins.NodeLaunchMethod.JNLP)

def worker_delete(node_name):
    j = jenkins.Jenkins(os.environ['JENKINS_URL'], os.environ['JENKINS_USER'], os.environ['JENKINS_PASS'])
    j.node_delete(node_name)

def worker_download(target):
    if os.path.isfile(worker_jar):
        os.remove(worker_jar)

    loader = urllib.URLopener()
    loader.retrieve(os.environ['JENKINS_URL'] + '/jnlpJars/worker.jar', '/var/lib/jenkins/worker.jar')

def worker_run(worker_jar, jnlp_url):
    params = [ 'java', '-jar', worker_jar, '-jnlpUrl', jnlp_url ]
    if os.environ['JENKINS_WORKER_ADDRESS'] != '':
        params.extend([ '-connectTo', os.environ['JENKINS_WORKER_ADDRESS' ] ])

    if os.environ['WORKER_SECRET'] == '':
        params.extend([ '-jnlpCredentials', os.environ['JENKINS_USER'] + ':' + os.environ['JENKINS_PASS'] ])
    else:
        params.extend([ '-secret', os.environ['WORKER_SECRET'] ])
    return subprocess.Popen(params, stdout=subprocess.PIPE)

def signal_handler(sig, frame):
    if process != None:
        process.send_signal(signal.SIGINT)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def host_ready(url):
    try:
        r = requests.head(url, verify=False, timeout=None)
        return r.status_code == requests.codes.ok
    except:
        return False

while not host_ready(worker_jar_url):
    print("Host not ready yet, sleeping for 10sec!")
    time.sleep(10)

worker_download(worker_jar)
print('Downloaded Jenkins worker jar.')

if os.environ['WORKER_WORKING_DIR']:
    os.setcwd(os.environ['WORKER_WORKING_DIR'])

if os.environ['CLEAN_WORKING_DIR'] == 'true':
    clean_dir(os.getcwd())
    print("Cleaned up working directory.")

if os.environ['WORKER_NAME'] == '':
    worker_create(worker_name, os.getcwd(), os.environ['WORKER_EXECUTORS'], os.environ['WORKER_LABELS'])
    print('Created temporary Jenkins worker.')

process = worker_run(worker_jar, jnlp_url)
print('Started Jenkins worker with name "' + worker_name + '" and labels [' + os.environ['WORKER_LABELS'] + '].')
process.wait()

print('Jenkins worker stopped.')
if os.environ['WORKER_NAME'] == '':
    worker_delete(worker_name)
    print('Removed temporary Jenkins worker.')
