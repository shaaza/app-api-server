from flask import Blueprint, jsonify
from sqlalchemy import create_engine

blueprint = Blueprint('labs_graphs', __name__)

sql_engine = create_engine('postgresql://ubuntu:electric123@localhost:5432/ubuntu')

########################################
#### GRAPH-DATA API for Labs ############
########################################

@blueprint.route('/labs/graphs')
def suggested_activities(lang, instance_no, goals_csv):
    data_to_send = { 'activities': 'hey' }
    return jsonify(data_to_send)