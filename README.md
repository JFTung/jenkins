# Jenkins on Docker

https://code-maze.com/ci-jenkins-docker/
https://github.com/CodeMazeBlog/docker-series/tree/docker-series-continuous-integration-jenkins-end

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

```
docker-compose up
http://localhost:8080
docker-compose down
```
