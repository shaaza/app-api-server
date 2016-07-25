from flask import Blueprint, jsonify
from sqlalchemy import create_engine
from test_kpis import test_kpis

blueprint = Blueprint('labs_data', __name__)

sql_engine = create_engine('postgresql://ubuntu:electric123@data.engazeapp.com:5432/ubuntu')

###################################
#### DATA API for LABS ############
###################################

@blueprint.route('/labs/data/testKpis')
def testKpis():
    data_to_send = test_kpis(sql_engine)
    return jsonify(data_to_send)