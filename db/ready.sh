#!/usr/bin/env bash
# Block until db is ready

# two lines of output:
#db_1      | 2018-03-05 01:45:26.543 UTC [35] LOG:  database system is ready to accept connections
#db_1      | 2018-03-05 01:45:28.555 UTC [1] LOG:  database system is ready to accept connections

TIMEOUT=10
for i in $(seq $TIMEOUT -1 1)
do
  RES=$(docker-compose logs db | grep 'ready to accept' | wc -l)
  if [ $RES = '2' ]
  then
    echo "DB connection is ready"
    exit 0
  fi
  echo "DB connection not ready, waiting another second"
  sleep 1
done

echo "DB connection timed out after $TIMEOUT seconds"
exit 1
