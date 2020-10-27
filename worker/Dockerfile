# NOTE: Only necessary if using Jenkins workers/nodes/agents

FROM ubuntu

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y apt-utils

RUN apt-get update && apt-get install -y git openjdk-8-jre python-is-python3 python3-pip
RUN pip3 install python-jenkins

RUN apt-get update && apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
RUN apt-key fingerprint 0EBFCD88
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
RUN apt-get update && apt-get install -y docker-ce docker-ce-cli containerd.io

RUN curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose

RUN mkdir -p /home/jenkins
RUN mkdir -p /var/lib/jenkins
COPY worker.py /var/lib/jenkins/worker.py
WORKDIR /home/jenkins

ENV JENKINS_URL "http://jenkins"
ENV JENKINS_WORKER_ADDRESS ""
ENV JENKINS_USER "admin"
ENV JENKINS_PASS "admin"
ENV WORKER_NAME ""
ENV WORKER_SECRET ""
ENV WORKER_EXECUTORS "1"
ENV WORKER_LABELS "docker"
ENV WORKER_WORKING_DIR ""
ENV CLEAN_WORKING_DIR "true"

CMD [ "python", "-u", "/var/lib/jenkins/worker.py" ]
