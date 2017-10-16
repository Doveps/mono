from flask import Flask, jsonify, request
from utils import SPcalls, DBconn
import sys, os
from app import app
from app import get_scanned, record, comparison
from app.base_path import get_path
from run_sql import execute_sql
import io, json, timeit, logging, datetime, psycopg2

spcalls = SPcalls()
now = datetime.datetime.now()


@app.route('/doveps/api/flavor/create/', methods=['POST'])
def create_flavors():
    filenames = request.files.getlist('files[]')
    get_scanned.get_items(filenames)
    record.record_base_flavors()

    return jsonify({"Status" : "OK", "Message" : "Saved"})

@app.route('/doveps/api/flavor/compare/', methods=['GET', 'POST'])
def compare():
    execute_sql("comparisons.sql")
    filenames = request.files.getlist('files[]')

    get_scanned.get_items(filenames)
    record.record_comparison_flavors()

    json_file = "Comparison-" + now.strftime("%Y-%m-%d_%H:%M") + ".json"

    new_packages =  json.dumps([{"Debs" : {"New" : comparison.new_debs()}},
                                {"Groups" : {"New" : comparison.new_groups()}},
                                {"Shadow" : {"New" : comparison.new_shadow()}},
                                {"Users" : {"New" : comparison.new_users()}}], indent=4, sort_keys=True)

    with io.open(json_file, 'w', encoding='utf-8') as data:
        data.write(unicode(new_packages))

    return new_packages

@app.route('/doveps/api/action/create/<json_file>/<name>/<resource>/<action>', methods=['GET'])
def create_action(json_file, name, resource, action):
    path = get_path() + "/mono/savant/app"
    os.chdir(path)

    with open('db_config.json', 'r') as db_file:
        db_info = json.load(db_file)

    db_name = db_info["database"]["database_name"]
    username = db_info["database"]["username"]
    password = db_info["database"]["password"]
    host = db_info["database"]["host"]
    engine_name = "postgresql://" + username + ":" + password + "@" + host + ":5432/" + db_name
    conn = psycopg2.connect(engine_name)
    cur = conn.cursor()
    
    if resource == 'Debs':
        cur.execute("select get_debs_id('" + name + "')")
    elif resource == 'Groups':
        cur.execute("select get_groups_id('" + name + "')")
    elif resource == 'Shadow':
        cur.execute("select get_shadow_id('" + name + "')")
    elif resource == 'Users':
        cur.execute("select get_users_id('" + name + "')")
        
    name_id = cur.fetchone()[0]
    name_id = int(name_id)

    cur.execute("select store_knowledge(%s, %s, %s, %s)", (name, resource, action, name_id))

    conn.commit()
    cur.close()
    conn.close()
     
    return jsonify({"Status" : "OK", "Message" : "Linked"})

@app.route('/doveps/api/debs/', methods=['GET'])
def show_debs():

    debs = spcalls.spcall('get_debs', ())
    entries = []
    print "length: ", len(debs)

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

    flavors = spcalls.spcall('get_flavors', ())
    entries = []
    print "length: ", len(flavors)

    if 'Error' in str(flavors[0][0]):
        return jsonify({'status': 'error',
                        'message': flavors[0][0]})

    elif len(flavors) != 0:
        for f in flavors:
            entries.append({"flavors": f[0]})

        return jsonify({"status": "OK", "message": "OK", "entries": entries, "count": len(entries)})

    else:
        return jsonify({"status": 'FAILED', "message": "Nothing Found"})

@app.route('/doveps/api/ansible/', methods=['GET'])
def show_ansible():

    scanned_files = spcalls.spcall('get_ansible_files', ())
    entries = []
    print "length: ", len(scanned_files)

    if 'Error' in str(scanned_files[0][0]):
        return jsonify({'status': 'error',
                        'message': scanned_files[0][0]})

    elif len(scanned_files) != 0:
        for s in scanned_files:
            entries.append({"scanned_files": s[0]})

        return jsonify({"status": "OK", "message": "OK", "entries": entries, "count": len(entries)})

    else:
        return jsonify({"status": 'FAILED', "message": "Nothing Found"})
