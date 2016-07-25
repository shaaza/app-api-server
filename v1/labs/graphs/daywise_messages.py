import datetime
import pandas
import urllib2, urllib
import json

def daywise_messages():
    start_day = datetime.date(2016, 7, 1)
    end_day = datetime.date.today()
    get_message_url = "http://beta.engazeapp.com/api/get/all/message/{0}%2000:00:00/{1}%2023:00:00".format(start_day, end_day)
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
    messages_day_count = messages_df.groupby(messages_df.good_time_start.dt.date).size()
    replied_message_df = messages_df[messages_df.message_reply != 0]
    replies_day_count = replied_message_df.groupby(replied_message_df.good_time_start.dt.date).size()
    dates = list(messages_day_count.index)
    x_ticks = [str(x) for x in dates]
    sent_count = list(messages_day_count)
    replies_count = list(replies_day_count)
    sent = [x - y for x, y in zip(sent_count, replies_count)]
    replies = replies_count
    percent = [round(y/float(x), 2) for x, y in zip(sent_count, replies_count)]
    replies_column = ['replies'] + replies
    sent_column = ['noreply'] + sent
    percent_column = ['percent'] + percent
    x_column = ['x'] + x_ticks
    total = ['total'] + sent_count
    data = [replies_column, sent_column, percent_column, x_column, total]
    return { "columns": data }

# HELPER

def return_pledge_type_id(row):
    pledge_type_id = int(row['message_text']['pledge_type_id'])
    return pledge_type_id

def return_message_reply(row):
    if row['reply_yes_no_noreply'] == None:
        reply = 0
    else:
        reply = int(row['reply_yes_no_noreply'])
    return reply