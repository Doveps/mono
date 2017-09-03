from flask import Flask, jsonify, request
from utils import SPcalls
import sys, os
from app import app
from app import get_scanned, record, comparison
from app.base_path import get_path
from run_sql import execute_sql

spcalls = SPcalls()


@app.route('/doveps/api/flavor/create/', methods=['POST'])
def create_flavors():
    filename = request.files['file']

    get_scanned.get_items(filename)

    record.record_base_flavors()

    filename.close()

    return jsonify({"Status" : "OK", "Message" : "Saved"})

@app.route('/doveps/api/flavor/compare/', methods=['GET', 'POST'])
def compare():
    execute_sql("comparisons.sql")
    filename = request.files['file']

    get_scanned.get_items(filename)
    record.record_comparison_flavors()

    if str(filename.filename).__contains__("debs"):
        return jsonify({"Debs" : {"New" : comparison.new_debs()}})

    elif str(filename.filename).__contains__("groups"):
        return jsonify({"Groups" : {"New" : comparison.new_groups()}})

    elif str(filename.filename).__contains__("shadow"):
        return jsonify({"Shadow" : {"New" : comparison.new_shadow()}})

    elif str(filename.filename).__contains__("users"):
        return jsonify({"Users" : {"New" : comparison.new_users()}})

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
