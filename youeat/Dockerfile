FROM  node:15.4.0-alpine3.10
WORKDIR /app
COPY ./package.json /app/
RUN yarn cache clean
RUN yarn install
RUN yarn global add @quasar/cli
ARG CACHE_DATE=not_a_date
COPY . /app/
ARG CACHE_DATE=not_a_date
RUN quasar build -m pwa
CMD ["quasar", "serve", "./dist/pwa", "-p", "5001"]
#CMD ["quasar", "dev", "-p", "5000"]





