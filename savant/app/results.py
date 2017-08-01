from flask import Flask, jsonify, request
from utils import *


spcalls = SPcalls()

@app.route('/doveps/api/store_imports/', methods=['POST'])
def store_imports(data):
	spcalls.spcall('store_import', (data,), True)

@app.route('/doveps/api/imports/', methods=['GET'])
def show_imports():

	imports = spcalls.spcall('get_imports', ())
	entries = []
	print "length: ", len(imports)

	if 'Error' in str(imports[0][0]):
		return jsonify({'status': 'error',
						'message': imports[0][0]})

	elif len(imports) != 0:
		for i in imports:
			entries.append({"imports": i[0]})

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