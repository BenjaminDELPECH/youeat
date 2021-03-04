
chmod +x Django/entryPoint.sh



docker-compose -f docker-compose-prod.yml down -v &&
docker-compose -f docker-compose-prod.yml build --no-cache &&
docker-compose -f docker-compose-prod.yml up -d --force-recreate

# docker-compose -f docker-compose.yml down -v
# docker-compose -f docker-compose.yml up --build --remove-orphans &
