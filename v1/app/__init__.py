from flask import Blueprint, render_template
from data import blueprint as data_blueprint
from graphs import blueprint as graphs_blueprint

data = data_blueprint
graphs = graphs_blueprint


