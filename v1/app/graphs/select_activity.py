import datetime
import pandas

################################################
#### RETURN GRAPH DATA (SELECT ACTIVITY) #######
################################################
def select_activity(instance_num, sqlengine):
    last_day = (datetime.date.today() - datetime.timedelta(days = 3))
    last = datetime.datetime.combine(last_day, datetime.time(23,0,0))
    first_day = last_day - datetime.timedelta(days = 30)
    first = datetime.datetime.combine(first_day, datetime.time(0,0,0))
    ###Fetch similar homes
    query = 'SELECT persons, hsize, htype FROM attr WHERE inst = {0};'.format(instance_num)
    details_df = pandas.read_sql_query(query,con=engine)
    details = list(details_df.iloc[0])
    query = 'SELECT inst FROM attr WHERE persons = \'{0}\' AND hsize = \'{1}\' AND htype = \'{2}\';'.format(details[0], details[1], details[2].encode('utf8'))
    inst_df = pandas.read_sql_query(query,con=engine)
    inst_list = list(inst_df['inst'])
    inst_list_query = str(tuple(inst_list)).rstrip(',)') + ')'
    ###Fetch co2 and consumption data
    query = "SELECT data.inst, avg(data.kwh) AS kwh, avg(data.kwh * co2_val_dk.value) AS co2 FROM data INNER JOIN co2_val_dk ON data.date = co2_val_dk.created_at WHERE data.inst IN {0} AND data.date BETWEEN \'{1}\' AND \'{2}\' GROUP BY data.inst;".format(inst_list_query, first, last)
    data_df = pandas.read_sql_query(query,con=sqlengine)
    data_df['kwh'] = data_df['kwh']*720
    data_df['co2'] = data_df['co2']*720
    your_home_kwh = int(data_df.loc[data_df.inst == instance_num, 'kwh'].iloc[0])
    your_home_co2 = int(data_df.loc[data_df.inst == instance_num, 'co2'].iloc[0])/1000
    similar_homes_kwh = int(data_df['kwh'].mean())
    similar_homes_co2 = int(data_df['co2'].mean())/1000
    ###Graph settings
    max_val_kwh = int(1.25*max(your_home_kwh, similar_homes_kwh))
    max_val_co2 = int(1.25*max(your_home_co2, similar_homes_co2))
    json_data = {
    "moneyGraphData": { "data": [ { "color": "#ffb76e", "data": { "x": "Similar Homes", "y": similar_homes_kwh } }, { "color": "#8BC34A", "data": { "x": "Your home", "y": your_home_kwh } } ], "settings": { "minValue": 0, "maxValue": max_val_kwh, "title": "null", "unit": "(kWh)" } },
    "localGraphData": { "benchmark": 35, "title": "null", "value": 45 },
    "co2GraphData": { "data": [ { "color": "#ffb76e", "data": { "x": "Similar homes", "y": similar_homes_co2 } }, { "color": "#8BC34A", "data": { "x": "Your home", "y": your_home_co2 } } ], "settings": { "minValue": 0, "maxValue": max_val_co2, "title": "null", "unit": "(kg)" } }
    }
    return json_data