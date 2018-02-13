sleep 5
rm -rf savant/app/db_config.json
touch savant/app/db_config.json
cat savant/app/db_config_travis.json >> savant/app/db_config.json
python savant/tests/test_basic.py
