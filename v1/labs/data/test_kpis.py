import datetime
import pandas
import urllib2, urllib
import json


def test_kpis(sqlengine):
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
	signups = len(list(messages_df.user_id.unique()))
	total_messages_sent = len(messages_df)
	replied_message_df = messages_df[messages_df.message_reply != 0]
	total_replies_received = len(replied_message_df)
	messages_day_count = messages_df.groupby(messages_df.good_time_start.dt.date).size()
	replies_day_count = replied_message_df.groupby(replied_message_df.good_time_start.dt.date).size()
	query = 'SELECT * FROM messages_reward;'
	reward_df = pandas.read_sql_query(query,con=sqlengine)
	yes_replies_reward_df = reward_df[reward_df.message_reply == 1]
	impact_points_awarded = yes_replies_reward_df.impact_points.sum()
	co2_footprint_reduced = yes_replies_reward_df.co2_reward.sum()
	kwh_reduced = yes_replies_reward_df[yes_replies_reward_df.pledge_type_id.isin([1, 2, 3, 5, 6, 9]) & (yes_replies_reward_df.kwh_change < 0)].kwh_change.sum()
	kwh_shifted = yes_replies_reward_df[~ yes_replies_reward_df.pledge_type_id.isin([1, 2, 3, 4, 5, 6, 9]) & (yes_replies_reward_df.kwh_change > 0)].kwh_change.sum()
	data = [
	[ "Sign-ups" , signups, "" ],
	[ "SMS Messages Sent" , total_messages_sent, "" ],
	[ "SMS Replies" , total_replies_received, "" ],
	[ "Impact Points Awarded" , impact_points_awarded, "" ],
	[ "CO2 Footprint Reduced" , co2_footprint_reduced/1000, "kg CO2-eq" ],
	[ "Consumption Reduced" , kwh_reduced, "kWh" ],
	[ "Consumption Shifted" , kwh_shifted, "kWh" ]
	]
	return data


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