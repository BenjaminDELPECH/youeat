#!/bin/bash
echo TEST SCRIPTS
# Remove old grafana volumes and data
docker container stop sitespeed_graphite_1
docker container stop sitespeed_grafana_1
docker volume rm performancedashboard_graphite performancedashboard_grafana

#get the docker compose file (with grafana) 
curl -O https://raw.githubusercontent.com/sitespeedio/sitespeed.io/main/docker/docker-compose.yml

# run the docker compose file

docker-compose -f docker-compose.yml up -d

# run specific tests 
#(dashboard http://127.0.0.1:3000)


docker run --shm-size 2g --rm -v "$(pwd):/sitespeed.io" --network=host sitespeedio/sitespeed.io:14.2.3 -b firefox https://simplenutrition.fr:443 -d=2  --sustainable.enable --graphite.host=localhost




#remove cocker containers and tests: 
#docker-compose stop && docker-compose rm



######################################################
# Types of tests
#MOBILE TESTING

#docker run --rm -v "$(pwd):/sitespeed.io" sitespeedio/sitespeed.io:14.2.3 https://mymail.simplenutrition.fr --mobile 

#firefox testing using crawler ( -d 2)
#docker run --rm -v /root:/sitespeed.io sitespeedio/sitespeed.io https://mymail.simplenutrition.fr -d 2 -b firefox



