FROM ubuntu

# Install Docker CLI in the agent
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y apt-transport-https ca-certificates curl gnupg
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
RUN echo "deb [arch=amd64] https://download.docker.com/linux/ubuntu xenial stable" > /etc/apt/sources.list.d/docker.list
RUN apt-get update && apt-get install -y docker-ce --allow-unauthenticated

RUN apt-get update && apt-get install -y curl git openjdk-8-jre

RUN apt-get update && apt-get install -y python
RUN curl https://bootstrap.pypa.io/get-pip.py --output get-pip.py
RUN python get-pip.py
#RUN pip install python-jenkins
#RUN pip install jenkins-webapi
RUN easy_install jenkins-webapi

# Get docker-compose in the agent container
RUN curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose
RUN mkdir -p /home/jenkins
RUN mkdir -p /var/lib/jenkins

# Start-up script to attach the worker to the host
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
