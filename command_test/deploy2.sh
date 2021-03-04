cp certs/prodkeys/* nginx/keys/
cp certs/prodkeys/* Django/
cp certs/prodkeys/* go_api/
chmod +x launchserver.sh
./launchserver.sh

cd ~/simplenutritionfullstack/simplenutritionfrontend3
yarn cache clean
yarn install
quasar build -m pwa
rm -rf ../nginx/dist
cp -r dist/ ../nginx/dist
cd ..
chmod +x ~/simplenutritionfullstack/RUN_DOCKER.sh
./RUN_DOCKER.sh

docker exec django_api python3 ./Django/manageProd.py makemigrations
docker exec django_api python3 ./Django/manageProd.py migrate

unzip mysql.zip
