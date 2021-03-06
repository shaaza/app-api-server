from flask import Blueprint, jsonify
from sqlalchemy import create_engine
from consumption_change_morning import morning_change
from daywise_messages import daywise_messages

blueprint = Blueprint('labs_graphs', __name__)

sql_engine = create_engine('postgresql://ubuntu:electric123@localhost:5432/ubuntu')

########################################
#### GRAPH-DATA API for Labs ############
########################################

@blueprint.route('/labs/graphs/consumptionChange/morning')
def morning_compare():
	data_to_send = morning_change(sql_engine)
	print data_to_send
	return jsonify(data_to_send)

@blueprint.route('/labs/graphs/messages/daywise')
def messages_data():
    data_to_send = daywise_messages()
    return jsonify(data_to_send)



#######################################################
#### OLD ROUTES FOR BACKWARD COMPATIBILITY ############
#######################################################

@blueprint.route('/stats/graphs/morningcompare')
def morning_compare2():
	data_to_send = morning_change(sql_engine)
	print data_to_send
	return jsonify(data_to_send)

@blueprint.route('/stats/messagereplies/day')
def messages_data2():
    data_to_send = daywise_messages()
    return jsonify(data_to_send)
