#!/bin/bash
set -e
 
clean_exit() {
    local error_code="$?"
    kill -9 $(jobs -p) >/dev/null 2>&1 || true
    rm -rf "$PGSQL_DATA"
    return $error_code
}
 
check_for_cmd () {
    if ! which "$1" >/dev/null 2>&1
    then
        echo "Could not find $1 command" 1>&2
        exit 1
    fi
}
 
wait_for_line () {
    while read line
    do
        echo "$line" | grep -q "$1" && break
    done < "$2"
    # Read the fifo for ever otherwise process would block
    cat "$2" >/dev/null &
}

sudo add-apt-repository "deb https://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main"
wget --quiet -O - https://postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add - 
sudo apt-get update
sudo apt-get remove libpq5
sudo apt-get install libpq-dev
sudo apt-get install postgresql-9.4
#sudo /usr/lib/postgresql/9.1/bin/initdb /usr/local/var/postgres

 
#check_for_cmd postgres
 
trap "clean_exit" EXIT
 
# Start PostgreSQL process for tests
PGSQL_DATA=`mktemp -d /tmp/PGSQL-XXXXX`
PGSQL_PATH=`pg_config --bindir`
${PGSQL_PATH}/initdb ${PGSQL_DATA}
mkfifo ${PGSQL_DATA}/out
${PGSQL_PATH}/postgres -F -k ${PGSQL_DATA} -D ${PGSQL_DATA} &> ${PGSQL_DATA}/out &
# Wait for PostgreSQL to start listening to connections
wait_for_line "database system is ready to accept connections" ${PGSQL_DATA}/out
export DB_TEST_URL="postgresql:///?host=${PGSQL_DATA}&dbname=template1"
 

python test_basics.py
