#!usr/bin/python2.7
from flask import Flask
from flask_cors import CORS

from app import data as app_data
from app import graphs as app_graphs

app = Flask(__name__)
app.register_blueprint(app_data)
app.register_blueprint(app_graphs)
CORS(app)
