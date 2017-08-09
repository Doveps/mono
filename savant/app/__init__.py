from flask import Flask
import os

app = Flask(__name__)
app.debug = True


from app.results import create_flavors