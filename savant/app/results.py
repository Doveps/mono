from flask import Flask, jsonify, request
import sys, os, logging, psycopg2
from app import app
from app import get_scanned, query
import io, json, timeit, logging, datetime, psycopg2
from pathlib2 import Path

now = datetime.datetime.now()
path = str(os.getcwd()).split("/mono", 1)[0]
logging.basicConfig(level=logging.WARNING, format='%(asctime)s : %(levelname)s : %(message)s')

with open('db_config.json', 'r') as db_file:
    db_info = json.load(db_file)

db_name = db_info["database"]["database_name"]
username = db_info["database"]["username"]
password = db_info["database"]["password"]
host = db_info["database"]["host"]
engine_name = "postgresql://" + username + ":" + password + "@" + host + ":5432/" + db_name
conn = psycopg2.connect(engine_name)
cur = conn.cursor()

@app.route('/doveps/api/flavor/create/', methods=['POST'])
def create_flavors():
    filenames = request.files.getlist('files[]')
    get_scanned.get_items(filenames)
    que_flavors = query.Query()
    que_flavors.record_flavors()

    return jsonify({"Status" : "OK", "Message" : "Saved"})

@app.route('/doveps/api/flavor/compare/', methods=['GET', 'POST'])
def compare():
    logging.debug('\nComparing\n')
    filenames = request.files.getlist('files[]')
    get_scanned.get_items(filenames)
    que_compare = query.Query()
    que_compare.record_flavors()

    json_file = "Comparison-" + now.strftime("%Y-%m-%d_%H:%M") + ".json"

    new_packages =  json.dumps([{"Debs" : {"New" : que_compare.new_debs()}},
                                {"Groups" : {"New" : que_compare.new_groups()}},
                                {"Shadow" : {"New" : que_compare.new_shadow()}},
                                {"Users" : {"New" : que_compare.new_users()}}], indent=4, sort_keys=True)

    with io.open(path + "/mono/savant/app/" + json_file, 'w', encoding='utf-8') as data:
        data.write(unicode(new_packages))

    return new_packages

@app.route('/doveps/api/action/create/<json_file>/<name>/<resource>/<action>', methods=['GET'])
def create_action(json_file, name, resource, action):
    que_records = query.Query()
    que_records.record_knowledge(json_file, name, resource, action)
     
    return jsonify({"Status" : "OK", "Message" : "Linked"})

@app.route('/doveps/api/count/', methods=['GET'])
def flavor_count():
    que_count = query.Query()

    return jsonify({"Count" : que_count.check_duplicates()})

@app.route('/doveps/api/debs/', methods=['GET'])
def show_debs():

    debs = spcalls.spcall('get_debs', ())
    entries = []

    if 'Error' in str(debs[0][0]):
        return jsonify({'status': 'error',
                        'message': debs[0][0]})

    elif len(debs) != 0:
        for deb in debs:
            entries.append({"ID" : deb[0],
                            "Stat" : deb[1],
                            "Name" : deb[2],
                            "Version" : deb[3],
                            "Architecture" : deb[4]})

        return jsonify({"status": "OK", "message": "OK", "entries": entries, "count": len(entries)})

    else:
        return jsonify({"status": 'FAILED', "message": "Nothing Found"})

@app.route('/doveps/api/flavors/', methods=['GET'])
def show_flavors():

    que_flavors = query.Query()

    duplicates = que_flavors.check_duplicates()

    return jsonify({'Duplicates' : duplicates})

@app.route('/doveps/api/count/debs/', methods=['GET'])
def count_debs():
    cur.execute("select count(*) from debs")
    debs_count = cur.fetchall()

    return jsonify({'Debs Count' : debs_count})

@app.route('/doveps/api/count/groups/', methods=['GET'])
def count_groups():
    cur.execute("select count(*) from groups")
    groups_count = cur.fetchall()

    return jsonify({'Groups Count' : groups_count})

@app.route('/doveps/api/count/shadow/', methods=['GET'])
def count_shadow():
    cur.execute("select count(*) from shadow")
    shadow_count = cur.fetchall()

    return jsonify({'Shadow Count' : shadow_count})

@app.route('/doveps/api/count/users/', methods=['GET'])
def count_users():
    cur.execute("select count(*) from users")
    users_count = cur.fetchall()

    return jsonify({'Users Count' : users_count})

@app.route('/doveps/api/ansible/', methods=['GET'])
def show_ansible():

    scanned_files = spcalls.spcall('get_ansible_files', ())
    entries = []

    if 'Error' in str(scanned_files[0][0]):
        return jsonify({'status': 'error',
                        'message': scanned_files[0][0]})

    elif len(scanned_files) != 0:
        for s in scanned_files:
            entries.append({"scanned_files": s[0]})

        return jsonify({"status": "OK", "message": "OK", "entries": entries, "count": len(entries)})

    else:
        return jsonify({"status": 'FAILED', "message": "Nothing Found"})
