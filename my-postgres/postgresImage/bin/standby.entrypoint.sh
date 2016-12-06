#!/bin/bash
set -e

chown -R postgres $PGDATA

echo ">>> Starting standby node..."

# Instance has been already set up

chmod g+s /run/postgresql
chown -R postgres /run/postgresql
echo replication command
echo PGPASSWORD=$REPLICATION_PASSWORD gosu postgres repmgr -h $REPLICATION_PRIMARY_HOST -U $REPLICATION_USER -d $REPLICATION_DB -D $PGDATA standby clone -F
PGPASSWORD=$REPLICATION_PASSWORD gosu postgres repmgr -h $REPLICATION_PRIMARY_HOST -U $REPLICATION_USER -d $REPLICATION_DB -D $PGDATA standby clone -F
echo End replication



if [ "${1:0:1}" = '-' ]; then
	set -- postgres "$@"
fi

if [ "$1" = 'postgres' ]; then
	exec gosu postgres "$@"
fi

exec "$@"
