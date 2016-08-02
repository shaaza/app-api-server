import datetime
import random
import pandas
import string
import urllib2, urllib
import json
from math import ceil


def morning_change(sqlengine):
    #### DATE AND TIME SETTINGS #################
    print "Inside function"
    test_start_day = datetime.date(2016, 7, 2)
    test_end_day = datetime.date.today() - datetime.timedelta(days = 4)
    start_dt = test_start_day - datetime.timedelta(days=42)
    start_dt = datetime.datetime.combine(start_dt, datetime.time(0, 0, 0))
    end_dt = test_end_day
    end_dt = datetime.datetime.combine(end_dt, datetime.time(23, 0, 0))
    print "before messages data"
    #### MESSAGES DATA ##########################
    get_message_url = "http://beta.engazeapp.com/api/get/all/message/{0}%2000:00:00/{1}%2000:00:00".format(test_start_day, test_end_day)
    response = urllib2.urlopen(get_message_url)
    data = json.load(response)
    messages_df = pandas.DataFrame(data['data'])
    messages_df['pledge_type_id'] = messages_df.apply(return_pledge_type_id, axis = 1)
    messages_df['message_reply'] = messages_df.apply(return_message_reply, axis = 1)
    messages_df['date'] = pandas.to_datetime(messages_df.good_time_start, format = '%Y-%m-%d %H:%M:%S').dt.date
    messages_df = messages_df[['id', 'message_reply', 'user_id', 'pledge_type_id', 'date']]
    messages_df.id = messages_df.id.astype(int)
    messages_df.user_id = messages_df.user_id.astype(int)
    messages_df = messages_df[messages_df.message_reply == 1]
    messages_df = messages_df[messages_df.pledge_type_id == 1]
    print "before user instance number"
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
    print "merge with inst number"
    #### MERGE WITH INST NUMBER #################
    messages_df.user_id = messages_df.user_id.astype(int)
    messages_df = messages_df.merge(user_inst_df, on = ['user_id'])
    #### CONSUMPTION DATA #######################
    inst_list = list(set(messages_df.user_inst))
    inst_list_query = str(tuple(inst_list)).rstrip(',)') + ')'
    print "before query"
    query = 'SELECT * FROM data WHERE inst IN {0} AND date BETWEEN \'{1}\' AND \'{2}\';'.format(inst_list_query, start_dt, end_dt)
    kwh_df = pandas.read_sql_query(query,con=sqlengine)
    #### FIND HOUR WISE CONSUMPTION #############
    print "after query"
    hourly_consumption_before = ['before']
    hourly_consumption_after = ['after']
    for hour in range(5, 12):
        hour_consumption_before_value = messages_df.apply(return_hour_consumption_before, axis = 1, kwh_df = kwh_df, hour = hour).sum()
        hourly_consumption_before.append(round(hour_consumption_before_value,1))
        hour_consumption_after_value = messages_df.apply(return_hour_consumption_after, axis = 1, kwh_df = kwh_df, hour = hour).sum()
        hourly_consumption_after.append(round(hour_consumption_after_value,1))
    c3_data = { 'columns': [hourly_consumption_before, hourly_consumption_after] }
    return c3_data


# HELPERS


def return_pledge_type_id(row):
    pledge_type_id = int(row['message_text']['pledge_type_id'])
    return pledge_type_id

def return_message_reply(row):
    if row['reply_yes_no_noreply'] == None:
        reply = 0
    else:
        reply = int(row['reply_yes_no_noreply'])
    return reply

def return_hour_consumption_after(row, kwh_df, hour):
    user_inst = row['user_inst']
    date = row['date']
    hour_consumption_after = kwh_df[(kwh_df.inst == user_inst) & (kwh_df.date.dt.date == date) & (kwh_df.date.dt.hour == hour)].iloc[0][3]
    return hour_consumption_after

def return_hour_consumption_before(row, kwh_df, hour):
    user_inst = row['user_inst']
    date = row['date']
    weekday = row['date'].weekday()
    hour_consumption_before = kwh_df[(kwh_df.inst == user_inst) & (kwh_df.date.dt.date != date) & (kwh_df.date.dt.hour == hour) & (kwh_df.date.dt.weekday == weekday)].kwh.mean()
    return hour_consumption_before