from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from test_kpis import test_kpis
from hourly_co2_denmark import co2_emissions_dk, update_co2_emissions_dk

blueprint = Blueprint('labs_data', __name__)

sql_engine = create_engine('postgresql://ubuntu:electric123@data.engazeapp.com:5432/ubuntu')

###################################
#### DATA API for LABS ############
###################################

@blueprint.route('/labs/data/testKpis')
def testKpis():
    data_to_send = test_kpis(sql_engine)
    return jsonify(data_to_send)

@blueprint.route('/labs/data/hourlyCO2Emissions/denmark/all')
def hourlyCO2Emissions():
    return co2_emissions_dk()

@blueprint.route('/labs/data/hourlyCO2Emissions/denmark', methods=['POST'])
def updateHourlyCO2Emissions():
    data = request.get_json()
    update_co2_emissions_dk(data['value'], data['time'])
    return "Success"