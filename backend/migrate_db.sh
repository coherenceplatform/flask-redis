#!/bin/bash

if [[ -z "${COHERENCE_DEV}" ]]; then
        COHERENCE_DEV="false"
else
        COHERENCE_DEV="${COHERENCE_DEV}"
fi

#echo "DB_NAME: $DB_NAME"
DB_SOCKET_NAME=$( compgen -A variable | grep DB1_SOCKET)
DB_ENDPOINT_NAME=$( compgen -A variable | grep DB1_ENDPOINT)
DB_INSTANCE_NAME=$( compgen -A variable | grep DB1_INSTANCE)
DB_PORT_NAME=$( compgen -A variable | grep DB1_PORT)

echo "DB_SOCKET_NAME: $DB_SOCKET_NAME"
echo "DB_ENDPOINT_NAME: $DB_ENDPOINT_NAME"
echo "DB_INSTANCE_NAME: $DB_INSTANCE_NAME"
echo "DB_PORT_NAME: $DB_PORT_NAME"

DB_SOCKET=""
if [[ ! -z "${DB_SOCKET_NAME}" ]]; then
        DB_SOCKET=${!DB_SOCKET_NAME}
fi

DB_ENDPOINT=""
if [[ ! -z "${DB_ENDPOINT_NAME}" ]]; then
        DB_ENDPOINT=${!DB_ENDPOINT_NAME}
fi

DB_INSTANCE=""
if [[ ! -z "${DB_INSTANCE_NAME}" ]]; then
        DB_INSTANCE=${!DB_INSTANCE_NAME}
fi

DB_PORT=""
if [[ ! -z "${DB_PORT_NAME}" ]]; then
        DB_PORT=${!DB_PORT_NAME}
fi

#echo "DB_SOCKET: $DB_SOCKET"
#echo "DB_INSTANCE: $DB_INSTANCE"

if [[ "${COHERENCE_DEV}" == "true" ]]
then
	if [[ ! -z "${DB_HOST}" ]]; then
        	POSTGRESQL_URL="postgres://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}?sslmode=disable"
	else
        	POSTGRESQL_URL="postgres://${DB_USER}:${DB_PASSWORD}@localhost:${DB_PORT}/${DB_NAME}?sslmode=disable"
	fi
else
	if [[ ! -z "${DB_ENDPOINT}" ]]; then
        	POSTGRESQL_URL="postgres://${DB_USER}:${DB_PASSWORD}@${DB_ENDPOINT}:${DB_PORT}/${DB_NAME}?sslmode=disable"
	else
        	POSTGRESQL_URL="postgres://${DB_USER}:${DB_PASSWORD}@/${DB_NAME}?host=${DB_SOCKET}"
	fi
fi

echo "POSTGRESQL_URL: $POSTGRESQL_URL"

flask db init
flask db migrate


