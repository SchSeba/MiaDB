#!/bin/bash

if [ -z "$CLUSTER_NODE_NETWORK_NAME" ]; then
    CLUSTER_NODE_NETWORK_NAME="`hostname`"
fi

echo "127.0.0.1 $CLUSTER_NODE_NETWORK_NAME" >> /etc/hosts
# Need this loopback to speedup connections and also k8s doesn't have DNS loopback by service name on the same pod

echo "cluster=$CLUSTER_NAME
node=$NODE_ID
node_name=$NODE_NAME
conninfo='user=$REPLICATION_USER password=$REPLICATION_PASSWORD host=$CLUSTER_NODE_NETWORK_NAME dbname=$REPLICATION_DB port=$REPLICATION_PRIMARY_PORT connect_timeout=2'
failover=automatic
promote_command='PGPASSWORD=$REPLICATION_PASSWORD repmgr standby promote --log-level DEBUG --verbose; echo $CLUSTER_NODE_NETWORK_NAME > /master'
follow_command='PGPASSWORD=$REPLICATION_PASSWORD repmgr standby follow -W --log-level DEBUG --verbose'
reconnect_attempts=3
reconnect_interval=5
master_response_timeout=20
loglevel=INFO
" >> /etc/repmgr.conf

chown postgres /etc/repmgr.conf
