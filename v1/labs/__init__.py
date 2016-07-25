from flask import Blueprint, render_template
from data import app_data as data_blueprint
from graphs import blueprint as graphs_blueprint

data = data_blueprint
graphs = Blueprint('app_graphs', __name__)


