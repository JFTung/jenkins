# Starting off with the Jenkins base Image
FROM jenkins/jenkins

# Installing the plugins we need using the in-built install-plugins.sh script
RUN /usr/local/bin/install-plugins.sh \
    blueocean \
    docker-workflow \
    git \
    workflow-aggregator

# Skip the initial setup wizard
ENV JAVA_OPTS -Djenkins.install.runSetupWizard=false

VOLUME ./jenkins-home:/var/jenkins_home
