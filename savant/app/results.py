from flask import Flask, jsonify, request
from utils import SPCalls


spcalls = SPcalls()

@app.route('/doveps/api/store_debs/', methods=['POST'])
def store_debs(stat, name, vers, arch):
	spcalls.spcall('store_debs', (stat, name, vers, arch,), True)

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