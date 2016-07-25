from flask import Blueprint, jsonify
from sqlalchemy import create_engine

from update_database import update_database
from csv_file_backup import backup_csv

crons = Blueprint('labs_graphs', __name__)

sql_engine = create_engine('postgresql://ubuntu:electric123@data.engazeapp.com:5432/ubuntu')

########################################
#### CRONS ############
########################################

@blueprint.route('/crons/updateDatabase', methods=['POST'])
def updateDatabase():
    date_to_send = update_database(sql_engine)
    return jsonify(data_to_send)

@blueprint.route('/crons/backupCSV/<string:folder>', methods=['POST'])
def backup_csv(folder):
    data_to_send = copy_file(folder)
    return jsonify(data_to_send)
