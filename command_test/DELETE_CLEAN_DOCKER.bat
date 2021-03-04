@ECHO OFF
FOR /f "tokens=*" %%i IN ('docker ps -q') DO docker stop %%i
docker rm $(docker ps -q -f status=exited)
docker rm $(docker ps -a -q)
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker container rm $(docker container ps -aq)
docker system prune
docker volume prune -f
docker network prune -f
docker system prune -a -f
docker system prune --volumes
