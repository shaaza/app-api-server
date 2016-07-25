#!usr/bin/python2.7
from flask import Flask
from flask_cors import CORS

from app import data as app_data
from app import graphs as app_graphs

from labs import data as labs_data
from labs import graphs as labs_graph

# from cron import crons

app = Flask(__name__)
app.register_blueprint(app_data)
app.register_blueprint(app_graphs)
app.register_blueprint(labs_data)
app.register_blueprint(labs_graphs)
CORS(app)
