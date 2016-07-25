from flask import Blueprint, render_template
from data import blueprint as labs_data_blueprint
from graphs import blueprint as labs_graphs_blueprint

data = labs_data_blueprint
graphs = labs_graphs_blueprint


