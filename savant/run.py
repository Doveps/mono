from flask import Flask
import os

from app import app
from app.run_sql import execute_sql

if __name__ == '__main__':
    app.run()