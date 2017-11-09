from flask import Flask, jsonify, request
import sys, os
from app import app
from app import get_scanned, query
from app.base_path import get_path
import io, json, timeit, logging, datetime, psycopg2

# spcalls = SPcalls()
now = datetime.datetime.now()

@app.route('/doveps/api/flavor/create/', methods=['POST'])
def create_flavors():
    filenames = request.files.getlist('files[]')
    get_scanned.get_items(filenames)
    query.record_base_flavors()

    return jsonify({"Status" : "OK", "Message" : "Saved"})

@app.route('/doveps/api/flavor/compare/', methods=['GET', 'POST'])
def compare():
    query.execute_sql("comparisons.sql")
    filenames = request.files.getlist('files[]')

    get_scanned.get_items(filenames)
    query.record_base_flavors()
    query.record_comparison_flavors()

    json_file = "Comparison-" + now.strftime("%Y-%m-%d_%H:%M") + ".json"

    new_packages =  json.dumps([{"Debs" : {"New" : query.new_debs()}},
                                {"Groups" : {"New" : query.new_groups()}},
                                {"Shadow" : {"New" : query.new_shadow()}},
                                {"Users" : {"New" : query.new_users()}}], indent=4, sort_keys=True)

    with io.open(json_file, 'w', encoding='utf-8') as data:
        data.write(unicode(new_packages))

    return new_packages

@app.route('/doveps/api/action/create/<json_file>/<name>/<resource>/<action>', methods=['GET'])
def create_action(json_file, name, resource, action):
    query.record_knowledge()
     
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
