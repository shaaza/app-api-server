import psycopg2
import json
from datetime import datetime, timedelta


def update_co2_emissions_dk(co2val, timestmp):
	conn = psycopg2.connect(dbname="ubuntu", user="ubuntu", host="data.engazeapp.com", password="electric123");
	cursor = conn.cursor()
	reading_time = timestmp + " Europe/Copenhagen"
	created_at = datetime.now() + timedelta(hours = 2)
	created_at = created_at.replace(microsecond=0, minute=0, second=0)
	cursor.execute('INSERT INTO co2_val_dk (reading_time, created_at, value) VALUES (%s,%s,%s)', (reading_time, created_at, co2val))
	conn.commit()
	conn.close()
	return True

def co2_emissions_dk():
	conn = psycopg2.connect(dbname="ubuntu", user="ubuntuco", host="data.engazeapp.com", password="electric123");
	cursor = conn.cursor()
	cursor.execute('SELECT id, reading_time, created_at, value FROM co2_val_dk')
	conn.commit()
	data = cursor.fetchall()
	conn.close()
	return json.dumps(data, default=date_handler)

# HELPERS

def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError