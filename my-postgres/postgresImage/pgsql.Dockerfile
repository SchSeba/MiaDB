FROM postgres:9.6

ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y postgresql-server-dev-9.6
RUN apt-get install -y postgresql-9.6-repmgr


COPY ./bin /usr/local/bin/cluster
RUN chmod -R +x /usr/local/bin/cluster && \
    ln -s /usr/local/bin/cluster/wait_db.sh /usr/local/bin/wait_db

COPY ./configs /var/cluster_configs

ENTRYPOINT ["/usr/local/bin/cluster/deploy.sh"]
