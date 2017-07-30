from flask import Flask
import os

from app import app
from app.results import *

if __name__ == '__main__':
    app.run()