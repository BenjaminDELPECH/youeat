#!/bin/bash
cd ~/simplenutritionfullstack/simplenutritionfrontend3 && yarn cache clean && yarn install && quasar build -m pwa && rm -rf ../nginx/dist && cp -r dist/ ../nginx/dist && cd .. && chmod +x ~/simplenutritionfullstack/RUN_DOCKER.sh && ./RUN_DOCKER.sh
