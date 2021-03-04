cp /etc/letsencrypt/live/simplenutrition.fr/* Django/
cp /etc/letsencrypt/live/simplenutrition.fr/* go_api/
cp /etc/letsencrypt/live/youeat.fr/* go_api2/
cp /etc/letsencrypt/live/youeat.fr/* Django/
cp /etc/letsencrypt/live/simplenutrition.fr/* nginx/keys/simplenutrition.fr/
cp /etc/letsencrypt/live/youeat.fr/* nginx/keys/youeat.fr/

cp /etc/letsencrypt/* nginx/keys

chmod +x ./Django/entryPoint.sh && docker-compose down
docker-compose build --no-cache quasar2
docker-compose up -d

