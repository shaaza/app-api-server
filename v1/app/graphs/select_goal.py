import json, random
import datetime
import pandas


############################################
#### RETURN GRAPH DATA (SELECT GOAL) #######
############################################
def select_goal(instance_num,sqlengine):
    last_day = (datetime.date.today() - datetime.timedelta(days = 3))
    last = datetime.datetime.combine(last_day, datetime.time(23,0,0))
    first_day = last_day - datetime.timedelta(days = 30)
    first = datetime.datetime.combine(first_day, datetime.time(0,0,0))
    ###Fetch co2 and consumption data
    query = "SELECT data.inst, avg(data.kwh) AS kwh, avg(data.kwh * co2_val_dk.value) AS co2 FROM data INNER JOIN co2_val_dk ON data.date = co2_val_dk.created_at WHERE data.date BETWEEN \'{0}\' AND \'{1}\' GROUP BY data.inst;".format(first, last)
    data_df = pandas.read_sql_query(query,con=sqlengine)
    data_df['kwh'] = data_df['kwh']*720
    data_df['co2'] = data_df['co2']*720
    your_home_kwh = int(data_df.loc[data_df.inst == instance_num, 'kwh'].iloc[0])
    your_home_co2 = int(data_df.loc[data_df.inst == instance_num, 'co2'].iloc[0])/1000
    typical_homes_kwh = int(data_df['kwh'].mean())
    typical_homes_co2 = int(data_df['co2'].mean())/1000
    ###Graph settings
    max_val_kwh = int(1.25*max(your_home_kwh, typical_homes_kwh))
    max_val_co2 = int(1.25*max(your_home_co2, typical_homes_co2))
    json_data = {
    "moneyGraphData": { "data": [ { "color": "#ffb76e", "data": { "x": "Typical Homes", "y": typical_homes_kwh } }, { "color": "#8BC34A", "data": { "x": "Your home", "y": your_home_kwh } } ], "settings": { "minValue": 0, "maxValue": max_val_kwh, "title": "null", "unit": "(kWh)" } },
    "localGraphData": { "benchmark": 35, "title": "null", "value": 45 },
    "co2GraphData": { "data": [ { "color": "#ffb76e", "data": { "x": "Typical homes", "y": typical_homes_co2} }, { "color": "#8BC34A", "data": { "x": "Your home", "y": your_home_co2 } } ], "settings": { "minValue": 0, "maxValue": max_val_co2, "title": "null", "unit": "(kg)" } }
    }
    return json_data