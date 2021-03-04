FROM  node:15.4.0-alpine3.10 as buildQuasarSimplenutrition
WORKDIR /app
COPY ./package.json /app/
RUN yarn cache clean
RUN yarn install
RUN yarn global add @quasar/cli
COPY . /app/
RUN quasar build -m pwa
CMD ["quasar", "serve", "./dist/pwa"]




