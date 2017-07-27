from flask import Flask, jsonify, request
from utils import *

spcalls = SPcalls()

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