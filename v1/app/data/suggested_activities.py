### COMMON DEPENDENCY
import pandas
import json
import datetime 
### list_suggested_activities
import random
### interval_specific_activity_ranking
import os ### REQUIRED??
import calendar ### REQUIRED??


#############################################
#### RETURN ACTIVITIES BASED ON GOALS #######
#############################################
def list_suggested_activities(goals, instance_num, lang, sqlengine):
    filename = os.path.join(os.path.dirname(__file__), 'json/activities_' + lang + '.json')
    with open(filename) as json_data:
        activities_data = json.load(json_data)
    last_day = (datetime.date.today() - datetime.timedelta(days = 3))
    last = datetime.datetime.combine(last_day, datetime.time(23,0,0))
    first_day = last_day - datetime.timedelta(days = 30)
    first = datetime.datetime.combine(first_day, datetime.time(0,0,0))
    goals = map(int,goals)
    rank_df = interval_specific_activity_ranking(instance_num, lang, sqlengine)
    intervalspecific = list(rank_df.activity)
    appliancespecific = [x['title'] for x in activities_data if x['appliance_specific'] == 1]
    speacialdays = [x['title'] for x in activities_data if x['special_days'] == 1]
    local = [x['title'] for x in activities_data if x['localChange'] == 1]
    co2 = [x['title'] for x in activities_data if x['co2Change'] == 1]
    money = [x['title'] for x in activities_data if x['moneyChange'] == 1]
    #### ACTIVTY SELECTION ######################
    m,c,l = goals[0], goals[1], goals[2]
    activity_list = []
    remaining = 6
    if (l == 1):
        activity_list = activity_list + local
        remaining = remaining - 1
    if ((c == 1) & (m == 0)):
        only_co2 = list(set(co2) - set(money))
        only_co2_appliancespecific = intersection(only_co2, appliancespecific)
        only_co2_specialdays = intersection(only_co2, speacialdays)
        activity_list = activity_list + only_co2_specialdays
        remaining = remaining - 2
        random.shuffle(only_co2_appliancespecific)
        activity_list = activity_list + only_co2_appliancespecific[0:remaining]
        remaining = 0
    if (m == 1):
        money_co2 = intersection(money, co2)
        money_co2_appliancespecific = intersection(money_co2, appliancespecific)
        activity_list = activity_list + money_co2_appliancespecific
        remaining = remaining - 2
        activity_list = activity_list + intervalspecific[0:remaining]
        remaining = 0
    random.shuffle(activity_list)
    random.shuffle(appliancespecific + intervalspecific)
    activity_list = activity_list + appliancespecific[0:remaining]
    #### ACTIVTY OUTPUT #########################
    suggested_activities = [x for x in activities_data if x['title'] in activity_list]
    for activity in suggested_activities:
        if activity['interval_specific'] == 1:
            activity_name = activity['title']
            activity['co2Change'] = -(rank_df.loc[rank_df.activity == activity_name, 'co2_savings'].iloc[0])/1000
            activity['moneyChange'] = -(rank_df.loc[rank_df.activity == activity_name, 'money_savings'].iloc[0])
            activity['localChange'] = 0
        elif activity['appliance_specific'] == 1:
            start_hour_str = activity['pledge']['startTime']
            end_hour_str = activity['pledge']['endTime']
            start_hour = datetime.datetime.strptime(start_hour_str, '%H:%M').hour
            end_hour = datetime.datetime.strptime(end_hour_str, '%H:%M').hour
            hour_range = str(tuple(range(start_hour, end_hour))).rstrip(',)') + ')'
            query = 'SELECT date_part(\'hour\', created_at) AS hour, avg(value) AS co2_avg FROM co2_val_dk WHERE date_part(\'hour\', created_at) IN {0} GROUP BY date_part(\'hour\', created_at) ORDER BY date_part(\'hour\', created_at);'.format(hour_range)
            co2_avg_df = pandas.read_sql_query(query,con=sqlengine)
            best_hour_value = co2_avg_df.co2_avg.min()
            mean_hour_value = co2_avg_df.co2_avg.mean()
            co2_diff = mean_hour_value - best_hour_value
            if activity['id'] in [6, 9]:
                co2_diff = mean_hour_value
            activity['co2Change'] = -(co2_diff * activity['co2Change'] * activity['activity_active_hours'] * activity['activity_frequency'] * activity['kwh_per_cycle'] * 30)/1000
            activity['moneyChange'] = -(activity['moneyChange'] * activity['activity_active_hours'] * activity['activity_frequency'] * activity['kwh_per_cycle'] * 30)
            activity['localChange'] = 0
        elif activity['special_days'] == 1:
            query = "SELECT date(data.date), avg(data.kwh) AS kwh, avg(co2_val_dk.value) AS co2 FROM data INNER JOIN co2_val_dk ON data.date = co2_val_dk.created_at WHERE data.inst = {0} AND data.date BETWEEN \'{1}\' AND \'{2}\' GROUP BY date(data.date);".format(instance_num, first, last)
            data_df = pandas.read_sql_query(query,con=sqlengine)
            data_df.sort_values(by = 'co2', inplace = True)
            co2_diff = data_df.co2.iloc[4:].mean() - data_df.co2.iloc[0:4].mean()
            activity['co2Change'] = -(activity['co2Change'] * co2_diff * data_df.kwh.iloc[0:4].mean() * 96 * 0.2)/1000
            activity['moneyChange'] = 0
            activity['localChange'] = (activity['localChange'] * 3)
        else:
            activity['co2Change'] = 0
            activity['moneyChange'] = 0
            activity['localChange'] = 0
    #### RETURN ACTIVTY LIST #########################
    return suggested_activities

#############################################
#### HELPER FUNCTIONS #######################
#############################################
def intersection(list1, list2):
    return [element for element in list1 if element in list2]


def interval_specific_activity_ranking(instance_num, lang, sqlengine):
    filename = os.path.join(os.path.dirname(__file__), 'json/activities_' + lang + '.json')
    with open(filename) as json_data:
        activities_data = json.load(json_data)
    query = 'SELECT persons, hsize, htype FROM attr WHERE inst = {0};'.format(instance_num)
    details_df = pandas.read_sql_query(query,con=sqlengine)
    details = list(details_df.iloc[0])
    #####
    query = 'SELECT inst FROM attr WHERE persons = \'{0}\' AND hsize = \'{1}\' AND htype = \'{2}\';'.format(details[0], details[1], details[2].encode('utf8'))
    inst_df = pandas.read_sql_query(query,con=sqlengine)
    inst_list = list(inst_df['inst'])
    #####
    past_days = 30
    last_day = (datetime.date.today() - datetime.timedelta(days = 3))
    last = datetime.datetime.combine(last_day, datetime.time(23,0,0))
    first_day = last_day - datetime.timedelta(days = past_days)
    first = datetime.datetime.combine(first_day, datetime.time(0,0,0))
    inst_list_query = str(tuple(inst_list)).rstrip(',)') + ')'
    #####
    query = "SELECT data.inst, data.date, data.kwh AS kwh, (data.kwh * co2_val_dk.value) AS co2 FROM data INNER JOIN co2_val_dk ON data.date = co2_val_dk.created_at WHERE data.inst IN {0} AND data.date BETWEEN \'{1}\' AND \'{2}\';".format(inst_list_query, first, last)
    data_df = pandas.read_sql_query(query,con=sqlengine)
    #####
    morning_user_kwh = data_df.loc[(data_df.inst == instance_num) & (data_df.date.dt.hour.isin([6, 7, 8])), 'kwh'].sum()
    morning_user_co2 = data_df.loc[(data_df.inst == instance_num) & (data_df.date.dt.hour.isin([6, 7, 8])), 'co2'].sum()
    morning_mean = data_df.loc[data_df.date.dt.hour.isin([6, 7, 8]), 'kwh'].groupby(data_df.inst).sum().mean()
    morning_std = data_df.loc[data_df.date.dt.hour.isin([6, 7, 8]), 'kwh'].groupby(data_df.inst).sum().std()
    #####
    evening_user_kwh = data_df.loc[(data_df.inst == instance_num) & (data_df.date.dt.hour.isin([17, 18, 19])), 'kwh'].sum()
    evening_user_co2 = data_df.loc[(data_df.inst == instance_num) & (data_df.date.dt.hour.isin([17, 18, 19])), 'co2'].sum()
    evening_mean = data_df.loc[data_df.date.dt.hour.isin([17, 18, 19]), 'kwh'].groupby(data_df.inst).sum().mean()
    evening_std = data_df.loc[data_df.date.dt.hour.isin([17, 18, 19]), 'kwh'].groupby(data_df.inst).sum().std()
    #####
    night_user_kwh = data_df.loc[(data_df.inst == instance_num) & (data_df.date.dt.hour.isin([20, 21, 22])), 'kwh'].sum()
    night_user_co2 = data_df.loc[(data_df.inst == instance_num) & (data_df.date.dt.hour.isin([20, 21, 22])), 'co2'].sum()
    night_mean = data_df.loc[data_df.date.dt.hour.isin([20, 21, 22]), 'kwh'].groupby(data_df.inst).sum().mean()
    night_std = data_df.loc[data_df.date.dt.hour.isin([20, 21, 22]), 'kwh'].groupby(data_df.inst).sum().std()
    #####
    weekend_user_kwh = data_df.loc[(data_df.inst == instance_num) & (data_df.date.dt.weekday.isin([5, 6])), 'kwh'].sum()
    weekend_user_co2 = data_df.loc[(data_df.inst == instance_num) & (data_df.date.dt.weekday.isin([5, 6])), 'co2'].sum()
    weekend_mean = data_df.loc[data_df.date.dt.weekday.isin([5, 6]), 'kwh'].groupby(data_df.inst).sum().mean()
    weekend_std = data_df.loc[data_df.date.dt.weekday.isin([5, 6]), 'kwh'].groupby(data_df.inst).sum().std()
    #####
    focus_user_kwh = data_df.loc[(data_df.inst == instance_num) & (data_df.date.dt.weekday.isin([6])), 'kwh'].sum()
    focus_user_co2 = data_df.loc[(data_df.inst == instance_num) & (data_df.date.dt.weekday.isin([6])), 'co2'].sum()
    focus_mean = data_df.loc[data_df.date.dt.weekday.isin([6]), 'kwh'].groupby(data_df.inst).sum().mean()
    focus_std = data_df.loc[data_df.date.dt.weekday.isin([6]), 'kwh'].groupby(data_df.inst).sum().std()
    #####
    all_activity_mean = (morning_mean + evening_mean + night_mean + weekend_mean + focus_mean)/5
    morning_x_value = abs(morning_user_kwh - morning_mean)/morning_std
    evening_x_value = abs(evening_user_kwh - evening_mean)/evening_std
    night_x_value = abs(night_user_kwh - night_mean)/night_std
    weekend_x_value = abs(weekend_user_kwh - weekend_mean)/weekend_std
    focus_x_value = abs(focus_user_kwh - focus_mean)/focus_std
    #####
    morning_y_value = morning_mean/all_activity_mean
    evening_y_value = evening_mean/all_activity_mean
    night_y_value = night_mean/all_activity_mean
    weekend_y_value = weekend_mean/all_activity_mean
    focus_y_value = focus_mean/all_activity_mean
    #####
    activity_name_list = [x['title'] for x in activities_data if x['interval_specific'] == 1]
    x_values = [morning_x_value, evening_x_value, night_x_value, weekend_x_value, focus_x_value]
    y_values = [morning_y_value, evening_y_value, night_y_value, weekend_y_value, focus_y_value]
    user_kwh_values = [morning_user_kwh, evening_user_kwh, night_user_kwh, weekend_user_kwh, focus_user_kwh]
    user_co2_values = [morning_user_co2, evening_user_co2, night_user_co2, weekend_user_co2, focus_user_co2]
    #####
    rank_df = pandas.DataFrame()
    rank_df['activity'] = activity_name_list
    rank_df['inst'] = instance_num
    alpha, beta = 0.66, 0.33
    rank_df['x_value'] = x_values
    rank_df['y_value'] = y_values
    rank_df['user_kwh_value'] = user_kwh_values
    rank_df['user_co2_value'] = user_co2_values
    rank_df['money_savings'] = rank_df['user_kwh_value'] * 0.1
    rank_df['co2_savings'] = rank_df['user_co2_value'] * 0.1
    rank_df['score'] = alpha*rank_df['x_value'] + beta*rank_df['y_value']
    rank_df.sort_values(by = 'score', ascending = False, inplace = True)
    return rank_df
