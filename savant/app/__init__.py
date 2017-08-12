from flask import Flask
import os
from app.run_sql import execute_sql

app = Flask(__name__)
app.debug = True


from app.results import create_flavors