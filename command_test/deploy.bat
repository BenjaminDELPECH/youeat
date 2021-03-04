


COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1

docker-compose -f docker-compose-prod.yml down -v
docker-compose -f docker-compose-prod.yml build --build-arg BUILDKIT_INLINE_CACHE=1
docker-compose -f docker-compose-prod.yml up -d --force-recreate

docker exec django_api python3 ./Django/manageProd.py makemigrations
docker exec django_api python3 ./Django/manageProd.py migrate

COPY /y certs\prodkeys\* nginx\keys\
COPY /y certs\prodkeys\* Django\
COPY /y certs\prodkeys\* go_api\

call refreshBestNutrientsFood.bat

cd simplenutritionfrontend3
quasar build -m pwa && cd ../ && Xcopy /E /I /Ys simplenutritionfrontend3\dist\pwa nginx\dist\pwa && docker restart nginx

