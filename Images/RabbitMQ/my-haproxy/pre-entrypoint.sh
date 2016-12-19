#!/bin/bash
set -e
CONFIG_FILE='/usr/local/etc/haproxy/haproxy.cfg'

echo ">>> Adding backends"
IFS=',' read -ra HOSTS <<< "$SERVERS"
for HOST in ${HOSTS[@]}
do

    IFS=':' read -ra INFO <<< "$HOST"

    HOST=""
    PORT="5672"

    [[ "${INFO[0]}" != "" ]] && HOST="${INFO[0]}"
    [[ "${INFO[1]}" != "" ]] && PORT="${INFO[1]}"

    echo ">>> Waiting for server  tcp://$HOST:$PORT to start rabbitmq"
    dockerize -wait tcp://$HOST:$PORT -timeout 250s

    HOSTIP=`dig $HOST +short`

    echo "
         server $HOST $HOSTIP:$PORT
" >> $CONFIG_FILE

done

exec ./docker-entrypoint.sh "$@"

sleep 30000