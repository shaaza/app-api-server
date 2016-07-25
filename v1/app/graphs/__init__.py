from flask import Blueprint, jsonify
from sqlalchemy import create_engine
from select_goal import select_goal

blueprint = Blueprint('app_graphs', __name__)

sql_engine = create_engine('postgresql://ubuntu:electric123@data.engazeapp.com:5432/ubuntu')

########################################
#### GRAPH-DATA API for App ############
########################################

@blueprint.route('/app/graphs/selectGoal/<int:instance_no>')
def selectGoal(instance_no):
    data_to_send = { 'graphData': select_goal(instance_no, sql_engine) }
    return jsonify(data_to_send)