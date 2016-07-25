from flask import Blueprint, jsonify
from sqlalchemy import create_engine
from consumption_change import morning_change

blueprint = Blueprint('labs_graphs', __name__)

sql_engine = create_engine('postgresql://ubuntu:electric123@data.engazeapp.com:5432/ubuntu')

########################################
#### GRAPH-DATA API for Labs ############
########################################

@blueprint.route('/labs/graphs/consumptionChange/morning')
def morning_compare():
    data_to_send = morning_change(sql_engine)
    return jsonify(data_to_send)
