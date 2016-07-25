import datetime
import random
import pandas
import string
import urllib2, urllib
import json
from math import ceil

#############################################
#### DATA FRAME TRANSFORM FUNCTIONS #########
#############################################
def return_pledge_type_id(row):
    pledge_type_id = int(row['message_text']['pledge_type_id'])
    return pledge_type_id

def return_message_reply(row):
    if row['reply_yes_no_noreply'] == None:
        reply = 0
    else:
        reply = int(row['reply_yes_no_noreply'])
    return reply

def return_user_kwh(row, end_dt, kwh_df):
    user_inst = row['user_inst']
    pledge_type_id = row['pledge_type_id']
    message_reply = row['message_reply']
    evaluation_start_hour = row['evaluation_start_time'].hour
    evaluation_end_hour = row['evaluation_end_time'].hour
    date = end_dt.date()
    hour_range = range(evaluation_start_hour, evaluation_end_hour)
    user_kwh = kwh_df.loc[(kwh_df.inst == user_inst) & (kwh_df.date.dt.hour.isin(hour_range)) & (kwh_df.date.dt.date == date)].kwh.sum()
    return user_kwh

def find_parameter_a(row, end_dt, kwh_df):
    user_inst = row['user_inst']
    evaluation_start_hour = row['evaluation_start_time'].hour
    evaluation_end_hour = row['evaluation_end_time'].hour
    date = end_dt.date()
    hour_range = range(evaluation_start_hour, evaluation_end_hour)
    parameter_a = kwh_df.loc[(kwh_df.inst == user_inst) & (kwh_df.date.dt.hour.isin(hour_range)) & (kwh_df.date.dt.date != date)].kwh.mean()*len(hour_range)
    return parameter_a

def find_parameter_b(row, end_dt, kwh_df):
    user_inst = row['user_inst']
    evaluation_start_hour = row['evaluation_start_time'].hour
    evaluation_end_hour = row['evaluation_end_time'].hour
    date = end_dt.date()
    hour_range = range(evaluation_start_hour, evaluation_end_hour)
    parameter_b = kwh_df.loc[(kwh_df.inst == user_inst) & (kwh_df.date.dt.hour.isin(hour_range)) & (kwh_df.date.dt.date != date)].groupby(kwh_df.date.dt.date).sum().kwh.std()
    return parameter_b

def return_kwh_change(row):
    mean = row['parameter_a']
    consumption = row['user_kwh']
    message_reply = row['message_reply']
    pledge_type_id = row['pledge_type_id']
    kwh_change = consumption - mean
    if ((pledge_type_id == 9) & (message_reply == 1)):
        kwh_change = -0.24
    if ((pledge_type_id == 9) & (message_reply != 1)):
        kwh_change = 0
    if ((pledge_type_id == 6) & (message_reply == 1)):
        kwh_change = -0.42
    if ((pledge_type_id == 6) & (message_reply != 1)):
        kwh_change = 0
    return kwh_change

def return_impact_points(row):
    kwh_change = row['kwh_change']
    mean = row['parameter_a']
    std = row['parameter_b']
    message_reply = row['message_reply']
    if std != 0:
        variation = abs(kwh_change)/std
    else:
        variation = 10
    pledge_type_id = row['pledge_type_id']
    impact_points = 1
    if ((pledge_type_id in [1, 2, 3, 4, 5]) & (kwh_change < 0)):
        if variation > 2:
            impact_points = 10
        else:
            impact_points = int(ceil(variation * 5))
    if ((pledge_type_id == 7) & (kwh_change >= 0.7)):
        impact_points = 10
    if ((pledge_type_id == 8) & (kwh_change >= 0.5)):
        impact_points = 10
    if ((pledge_type_id in [11, 12, 14, 15]) & (variation > 1) & (kwh_change > 0)):
        if variation > 2:
            impact_points = 10
        else:
            int(ceil(5 * (variation - 1))) + 5
    impact_points = impact_points + 5
    return impact_points

def return_co2_coeff(row, co2_df):
    average_denamark_co2 = 205
    pledge_type_id = row['pledge_type_id']
    pledge_start_hour = row['pledge_start_time'].hour
    pledge_end_hour = row['pledge_end_time'].hour
    good_hour_start = row['good_time_start'].hour
    good_hour_end = row['good_time_end'].hour
    hour_range = range(pledge_start_hour, pledge_end_hour)
    co2_good_hour = co2_df.loc[co2_df.date.dt.hour == good_hour_start].iloc[0][1]
    co2_hour_range = co2_df.loc[co2_df.date.dt.hour.isin(hour_range), 'value'].mean()
    if pledge_type_id in [1, 2, 3, 4, 5, 6, 9]:
        co2_coeff = co2_hour_range
    if pledge_type_id in [14, 15, 16]:
        co2_coeff = average_denamark_co2 - co2_hour_range
    if pledge_type_id in [7, 8, 10, 11, 12, 13]:
        co2_coeff = co2_hour_range - co2_good_hour
    return co2_coeff

def return_co2_reward(row):
    co2_coeff = row['co2_coeff']
    kwh_change = row['kwh_change']
    co2_reward = co2_coeff * kwh_change
    pledge_type_id = row['pledge_type_id']
    if pledge_type_id in [1, 2, 3, 4, 5, 6, 9]:
        if co2_reward > 0:
            co2_reward = 0
    if pledge_type_id in [7, 8, 10, 11, 12, 13, 14, 15, 16]:
        if co2_reward < 0:
            co2_reward = 0
    co2_reward = abs(co2_reward)
    return co2_reward

def find_parameter_c(row):
    kwh_change = row['kwh_change']
    mean = row['parameter_a']
    parameter_c = abs(kwh_change) * 100/mean
    return parameter_c

def return_reward_df(sqlengine):
    #### DATE AND TIME SETTINGS #################
    messages_start_day = datetime.datetime.utcnow().date() - datetime.timedelta(days=2)
    messages_end_day = messages_start_day + datetime.timedelta(days = 1)
    start_dt = messages_start_day - datetime.timedelta(days=42)
    start_dt = datetime.datetime.combine(start_dt, datetime.time(0, 0, 0))
    end_dt = messages_start_day
    end_dt = datetime.datetime.combine(end_dt, datetime.time(23, 0, 0))
    weekday = start_dt.isoweekday()
    #### CO2 DATA ###############################
    query = 'SELECT created_at, value FROM co2_val_dk WHERE date(created_at) = \'{0}\';'.format(messages_start_day)
    co2_df = pandas.read_sql_query(query,con=sqlengine)
    co2_df = co2_df.drop_duplicates()
    co2_df.columns = ['date', 'value']
    co2_df.index = range(0, 24)
    co2_df.date = co2_df.date.astype(str)
    co2_df.date = co2_df.date.apply(lambda x: str(x[0:13]))
    co2_df.date = pandas.to_datetime(co2_df.date, format = '%Y-%m-%dT%H')
    #### MESSAGES DATA ##########################
    get_message_url = "http://beta.engazeapp.com/api/get/all/message/{0}%2000:00:00/{1}%2000:00:00".format(messages_start_day, messages_end_day)
    response = urllib2.urlopen(get_message_url)
    data = json.load(response)
    messages_df = pandas.DataFrame(data['data'])
    messages_df['pledge_type_id'] = messages_df.apply(return_pledge_type_id, axis = 1)
    messages_df['message_reply'] = messages_df.apply(return_message_reply, axis = 1)
    messages_df = messages_df[['id', 'message_reply', 'user_id', 'pledge_type_id', 'pledge_start_time', 'pledge_end_time', 'good_time_start', 'good_time_end']]
    messages_df.id = messages_df.id.astype(int)
    messages_df.user_id = messages_df.user_id.astype(int)
    messages_df.good_time_start = pandas.to_datetime(messages_df.good_time_start, format = '%Y-%m-%d %H:%M:%S')
    messages_df.good_time_end = pandas.to_datetime(messages_df.good_time_end, format = '%Y-%m-%d %H:%M:%S')
    messages_df.pledge_start_time = pandas.to_datetime(messages_df.pledge_start_time, format = '%H:%M:%S')
    messages_df.pledge_end_time = pandas.to_datetime(messages_df.pledge_end_time, format = '%H:%M:%S')
    messages_df['evaluation_start_time'] = messages_df['pledge_start_time']
    messages_df.loc[messages_df.pledge_type_id.isin([6, 7, 8, 13, 14, 15, 16]), 'evaluation_start_time'] = messages_df.loc[messages_df.pledge_type_id.isin([6, 7, 8, 13, 14, 15, 16]), 'good_time_start']
    messages_df['evaluation_end_time'] = messages_df['pledge_end_time']
    messages_df.loc[messages_df.pledge_type_id.isin([6, 13, 14, 15, 16]), 'evaluation_end_time'] = messages_df.loc[messages_df.pledge_type_id.isin([6, 13, 14, 15, 16]), 'evaluation_start_time'] + datetime.timedelta(hours = 1)
    messages_df.loc[messages_df.pledge_type_id.isin([7, 8]), 'evaluation_end_time'] = messages_df.loc[messages_df.pledge_type_id.isin([7, 8]), 'evaluation_start_time'] + datetime.timedelta(hours = 2)
    #### USER INSTANCE NUMBER ###################
    get_inst_url = "http://beta.engazeapp.com/api/get/all/installation/number"
    response = urllib2.urlopen(get_inst_url)
    data = json.load(response)
    user_inst_df = pandas.DataFrame(data)
    user_inst_df = user_inst_df[['user_id', 'installation_number']]
    user_inst_df.columns = ['user_id', 'user_inst']
    user_inst_df = user_inst_df[pandas.notnull(user_inst_df.user_id)]
    user_inst_df.user_id = user_inst_df.user_id.astype(int)
    user_inst_df.user_inst = user_inst_df.user_inst.astype(int)
    #### MERGE WITH INST NUMBER #################
    messages_df.user_id = messages_df.user_id.astype(int)
    messages_df = messages_df.merge(user_inst_df, on = ['user_id'])
    #### CONSUMPTION DATA #######################
    inst_list = list(set(messages_df.user_inst))
    inst_list_query = str(tuple(inst_list)).rstrip(',)') + ')'
    query = 'SELECT * FROM data WHERE inst IN {0} AND date_part(\'isodow\', date) = {1} AND date BETWEEN \'{2}\' AND \'{3}\';'.format(inst_list_query, weekday, start_dt, end_dt)
    kwh_df = pandas.read_sql_query(query,con=sqlengine)
    #### FIND CHANGE PARAMETERS #################
    messages_df['user_kwh'] = messages_df.apply(return_user_kwh, axis = 1, end_dt = end_dt, kwh_df = kwh_df)
    messages_df['parameter_a'] = messages_df.apply(find_parameter_a, axis = 1, end_dt = end_dt, kwh_df = kwh_df)
    messages_df['parameter_b'] = messages_df.apply(find_parameter_b, axis = 1, end_dt = end_dt, kwh_df = kwh_df)
    messages_df['kwh_change'] = messages_df.apply(return_kwh_change, axis = 1)
    messages_df['impact_points'] = messages_df.apply(return_impact_points, axis = 1)
    messages_df['co2_coeff'] = messages_df.apply(return_co2_coeff, axis = 1, co2_df = co2_df)
    messages_df['co2_reward'] = messages_df.apply(return_co2_reward, axis = 1)
    messages_df['parameter_c'] = messages_df.apply(find_parameter_c, axis = 1)
    messages_df['message_id'] = messages_df['id']
    messages_reward_df = [['message_id', 'message_reply', 'impact_points', 'kwh_change', 'parameter_a', 'parameter_b', 'parameter_c' ]]
    messages_reward_df.to_sql(name='messages_reward', con=sqlengine, if_exists = 'append', index=False)
    update_df = messages_df[['id', 'user_id', 'co2_reward', 'impact_points', 'kwh_change']]
    return update_df

#############################################
#### UPDATE MESSAGES TABLE ##################
#############################################
def update_message_reward(sqlengine):
    update_df = return_reward_df(sqlengine)
    url = "http://beta.engazeapp.com/api/message/post/update/request"
    url2 = "http://beta.engazeapp.com/api/customer/impactpoint/update/request"
    for index, id, user_id, co2_reward, impact_points, kwh_change in update_df.itertuples():
        data_dict = {"id": id, "co2_reward": co2_reward, "impact_points_change": impact_points, "kwh_change":kwh_change}
        data_dict2 = {"user_id" : user_id, "impact_event_id": 19, "impact_points": impact_points - 5}
        data = urllib.urlencode(data_dict)
        data2 = urllib.urlencode(data_dict2)
        request = urllib2.Request(url, data)
        response = urllib2.urlopen(request)
        request = urllib2.Request(url2, data2)
        response = urllib2.urlopen(request)    