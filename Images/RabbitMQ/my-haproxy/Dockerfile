FROM haproxy:1.6
ENV DOCKERIZE_VERSION v0.2.0

RUN apt-get update
RUN apt-get install -y dnsutils wget
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
COPY pre-entrypoint.sh /

ENTRYPOINT ["/pre-entrypoint.sh"]
CMD ["haproxy", "-f", "/usr/local/etc/haproxy/haproxy.cfg"]
