from flask import Flask, jsonify, request
from utils import *

spcalls = SPcalls()

@app.route('/doveps/api/imports', methods=['GET'])
def show_imports():

	imports = spcalls.spcall('get_imports', ())
	entries = []

	if 'Error' in str(imports[0][0]):
		return jsonify({'status': 'error',
						'message': imports[0][0]})

	elif len(imports) != 0:
		# entris.append({})
		return jsonify({'haha':'haha'})