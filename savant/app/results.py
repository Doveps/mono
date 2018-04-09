from flask import Flask, jsonify, request
import sys, os, logging
from app import app
from app import get_scanned, query
import io, json, timeit, logging, datetime, psycopg2
from pathlib2 import Path

now = datetime.datetime.now()
path = str(os.getcwd()).split("/mono", 1)[0]
logging.basicConfig(level=logging.WARNING, format='%(asctime)s : %(levelname)s : %(message)s')

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

    return jsonify({"Count" : que_count.null_cases()})

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

    que_flavors = query.Query()

    debs_count = que_flavors.count_debs()
    groups_count = que_flavors.count_groups()
    shadow_count = que_flavors.count_shadow()
    users_count = que_flavors.count_users()

    duplicates = que_flavors.null_cases()

    total_debs = que_flavors.total_saved_debs()
    total_groups = que_flavors.total_saved_groups()
    total_shadow = que_flavors.total_saved_shadow()
    total_users = que_flavors.total_saved_users()

    print "Debs count: ", debs_count
    print "Groups count: ", groups_count
    print "Shadow count: ", shadow_count
    print "Users count: ", users_count

    return jsonify({'Debs' : debs_count, 'Groups' : groups_count,
                    'Shadow' : shadow_count, 'Users' : users_count,
                    'Total Debs' : total_debs, 'Total Groups' : total_groups,
                    'Total Shadow' : total_shadow, 'Total Users' : total_users,
                    'Duplicates' : duplicates})



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
