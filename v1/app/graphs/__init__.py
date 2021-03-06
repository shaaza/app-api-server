from flask import Blueprint, jsonify
from sqlalchemy import create_engine

from select_goal import select_goal
from select_activity import select_activity
from weekly_performance import weekly_performance

blueprint = Blueprint('app_graphs', __name__)

sql_engine = create_engine('postgresql://ubuntu:electric123@localhost:5432/ubuntu')

########################################
#### GRAPH-DATA API for App ############
########################################

@blueprint.route('/app/graphs/selectGoal/<int:instance_no>')
def selectGoal(instance_no):
    data_to_send = { 'graphData': select_goal(instance_no, sql_engine) }
    return jsonify(data_to_send)

@blueprint.route('/app/graphs/selectActivity/<int:instance_no>')
def selectActivity(instance_no):
    data_to_send = { 'graphData': select_activity(instance_no, sql_engine) }
    return jsonify(data_to_send)

@blueprint.route('/app/graphs/weeklyPerformance/<int:instance_no>')
def weeklyPerformance(instance_no):
    data_to_send = weekly_performance(instance_no, sql_engine)
    return jsonify(data_to_send)

#######################################################
#### OLD ROUTES FOR BACKWARD COMPATIBILITY ############
#######################################################


@blueprint.route('/goalGraphData/<int:instance_num>')
def selectGoal2(instance_num):
    data_to_send = { 'graphData': select_goal(instance_num, sql_engine) }
    return jsonify(data_to_send)

@blueprint.route('/graphData/<int:instance_num>')
def selectActivity2(instance_num):
    data_to_send = { 'graphData': select_activity(instance_num, sql_engine) }
    return jsonify(data_to_send)

@blueprint.route('/performanceGraphData/<int:instance_num>')
def weeklyPerformance2(instance_num):
    data_to_send = weekly_performance(instance_num, sql_engine)
    return jsonify(data_to_send)