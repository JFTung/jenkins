# Jenkins on Docker

## Building

```
cd host
docker build -t jenkins-host .
cd ..
```

Only if using Jenkins workers/nodes/agents:

```
cd worker
docker build -t jenkins-worker .
cd ..
```

## Running

Start Jenkins:

```
docker-compose up
```

Navigate to `http://localhost:9090` to access Jenkins. Once you're done, stop
Jenkins:

```
docker-compose down
```

## Configuration

All configuration changes made through the Jenkins web app will be saved in
[`./jenkins_home/`](jenkins_home). For example, when you first run Jenkins, you
should create an admin user and restrict access to logged-in users.
