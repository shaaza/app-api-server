from shutil import copyfile
# from os import path
from datetime import date

def backup_csv(folder):
	today = date.today()
	filename = str(today.day) + "-" + str(today.month) + "-" + str(today.year) + ".csv"
	copyfile("/home/seftp/EngazeDataSE.csv", "/home/ubuntu/data/se-csv-data/"+ folder + "/" + filename)
	# copystatus = path.exists("/home/ubuntu/data/se-csv-data/" + filename)
	return "Completed"