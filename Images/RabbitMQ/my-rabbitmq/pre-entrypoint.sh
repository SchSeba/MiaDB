#!/bin/bash
set -e

mkdir -p /var/lib/rabbitmq

if [ "$ERLANG_COOKIE" ]; then
    cookieFile='/var/lib/rabbitmq/.erlang.cookie'

    echo "$ERLANG_COOKIE" > "$cookieFile"
    chmod 600 "$cookieFile"
    chown rabbitmq "$cookieFile"

fi

chown rabbitmq:rabbitmq /var/lib/rabbitmq
exec gosu rabbitmq ./docker-entrypoint.sh "$@"