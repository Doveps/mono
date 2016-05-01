from flask import Flask
from flask.ext import restful
from flask.ext.restful import Api

import savant.snapshot

app = Flask(__name__)
api = restful.Api(app)

# allow cross-site connections
# http://www.davidadamojr.com/handling-cors-requests-in-flask-restful-apis/
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  # once savant-web app is working properly
  # http://stackoverflow.com/questions/19322973/security-implications-of-adding-all-domains-to-cors-access-control-allow-origin
  #response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8000')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

api.add_resource(savant.snapshot.SnapshotsAPI, '/snapshots')
