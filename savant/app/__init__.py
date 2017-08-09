from flask import Flask
import os

app = Flask(__name__)
app.debug = True


from app.results import create_flavor, show_debs, show_flavors, show_ansible
