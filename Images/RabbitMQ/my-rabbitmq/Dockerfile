FROM rabbitmq:3.6.6-management
ENV DOCKERIZE_VERSION v0.2.0

RUN apt-get update
RUN apt-get install -y dnsutils wget
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

COPY rabbitmq-cluster /usr/local/bin/
COPY pre-entrypoint.sh /


ENTRYPOINT ["/pre-entrypoint.sh"]
CMD ["rabbitmq-cluster"]
