from flask import Blueprint, jsonify
from suggested_activities import list_suggested_activities

blueprint = Blueprint('app_data', __name__)

sql_engine = create_engine('postgresql://ubuntu:electric123@data.engazeapp.com:5432/ubuntu')

###################################
#### DATA API for LABS ############
###################################

@blueprint.route('/app/data/activities/<string:lang>/<int:instance_no>/<string:goals_csv>')
def suggested_activities(lang, instance_no, goals_csv):
	## ADD ERROR HANDLING HERE ##
    if goals_csv is None:
        goals_csv = "1,1,1"
    ## ADD ERROR HANDLING HERE ##
    goal = goals_csv.split(",")
    activities  = list_suggested_activities(goal, instance_no, lang, sql_engine)
    data_to_send = { 'activities': activities }
    return jsonify(data_to_send)