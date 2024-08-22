FROM drone/drone:latest as base
ARG VERSION


ENV DRONE_GITEA_SERVER=https://full-enormous-crow.ngrok-free.app
ENV DRONE_SERVER_PROTO=http
ENV DRONE_TLS_AUTOCERT=false
ENV DRONE_COOKIE_SECRET=morten
ENV DRONE_COOKIE_TIMEOUT=720h
ENV DRONE_LOGS_DEBUG=true

RUN apk add --update --no-cache python3 py3-pip && \
    ln -sf python3 /usr/bin/python && \
    python3 --version

RUN python3 -m pip install --ignore-installed distlib --no-cache-dir pipenv==2022.8.30
RUN apk add --update curl
RUN apk add --no-cache --upgrade bash

COPY Pipfile* /config/
RUN cd /config && pipenv install --system --deploy && cd ..

RUN apk add --update jq

COPY . /config/

ENTRYPOINT ["config/start.sh"]