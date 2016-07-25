from flask import Blueprint, render_template
from data import blueprint as app_data_blueprint
from graphs import blueprint as app_graphs_blueprint

data = app_data_blueprint
graphs = app_graphs_blueprint


