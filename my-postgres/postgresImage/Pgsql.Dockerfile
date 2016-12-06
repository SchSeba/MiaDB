FROM postgres:9.6

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y postgresql-server-dev-9.6 && apt-get install -y postgresql-9.6-repmgr

COPY /bin/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

COPY ./configs /var/cluster_configs

WORKDIR /usr/local/bin/cluster/

COPY ./bin /usr/local/bin/cluster
RUN chmod -R +x /usr/local/bin/cluster && \
    ln -s /usr/local/bin/cluster/wait_db.sh /usr/local/bin/wait_db

ENTRYPOINT ["/usr/local/bin/cluster/deploy.sh"]
