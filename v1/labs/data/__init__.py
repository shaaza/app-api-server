from flask import Blueprint, jsonify
from sqlalchemy import create_engine

blueprint = Blueprint('labs_data', __name__)

sql_engine = create_engine('postgresql://ubuntu:electric123@data.engazeapp.com:5432/ubuntu')

###################################
#### DATA API for LABS ############
###################################

@blueprint.route('/labs/data/kpis')
def suggested_activities(lang, instance_no, goals_csv):
    data_to_send = { 'activities': 'hey' }
    return jsonify(data_to_send)