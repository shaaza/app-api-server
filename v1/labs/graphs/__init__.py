from flask import Blueprint, jsonify
from sqlalchemy import create_engine
from consumption_change_morning import morning_change
from daywise_messages import daywise_messages

blueprint = Blueprint('labs_graphs', __name__)

sql_engine = create_engine('postgresql://ubuntu:electric123@data.engazeapp.com:5432/ubuntu')

########################################
#### GRAPH-DATA API for Labs ############
########################################

@blueprint.route('/labs/graphs/consumptionChange/morning')
def morning_compare():
	print "Inside route handler"
	data_to_send = morning_change(sql_engine)
	print "After call, in handler"
	return jsonify(data_to_send)

@blueprint.route('/labs/graphs/messages/daywise')
def messages_data():
    data_to_send = daywise_messages()
    return jsonify(data_to_send)