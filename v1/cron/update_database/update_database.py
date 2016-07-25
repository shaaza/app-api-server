import pandas
import datetime
from change_detect import update_message_reward



def update_database(sqlengine):
    #### CHECK LATEST UPDATE DATETIME ###########
    query = "SELECT max(date) FROM data WHERE status = 0;"
    latest_date_df = pandas.read_sql_query(query, con=sqlengine)
    latest_date = latest_date_df.iloc[0][0].date()
    #### DATE AND TIME SETTINGS #################
    date = (datetime.datetime.today() - datetime.timedelta(days = 2)).strftime('%Y-%m-%d')
    dt_series = pandas.date_range(date, periods = 24, freq = '1H')
    dt_range = pandas.DataFrame()
    dt_range['dt_range'] = [x.to_datetime() for x in dt_series]
    all_dates = list(dt_range.dt_range)
    #### ALL CONSUMPTION DATA ###################
    query = "SELECT * FROM data WHERE date >= \'2016-05-01 00:00:00\' AND status = 0;"
    df = pandas.read_sql_query(query, con=sqlengine)
    #### TODAYS CONSUMPTION DATA ################
    kwh_df = pandas.read_csv('/home/seftp/EngazeDataSE.csv')
    kwh_df = kwh_df[['instnr', 'Dato', 'kWh']]
    kwh_df.columns = ['inst', 'date', 'kwh']
    kwh_df = kwh_df.drop_duplicates()
    kwh_df.date = pandas.to_datetime(kwh_df.date, format = '%Y-%m-%d %H')
    kwh_df['status'] = 0
    file_date = kwh_df.date.dt.date[0]
    if file_date > latest_date:
        #### FILL MISSING INST DATA #################
        inst_list = kwh_df.inst.unique()
        complete_list = df.inst.unique()
        missing_inst = [x for x in complete_list if x not in inst_list]
        missing_inst_df = pandas.DataFrame()
        for inst in missing_inst:
            fill_inst = pandas.DataFrame()
            fill_inst['date'] = dt_range
            fill_inst['inst'] = inst
            missing_inst_df = missing_inst_df.append(fill_inst, ignore_index = True)
        if missing_inst != []:
            missing_inst_df['status'] = 1
            missing_inst_df['kwh'] = missing_inst_df.apply(fill_hour_mean, axis = 1, df = df)
            missing_inst_df = missing_inst_df[['inst', 'date', 'kwh', 'status']]
            kwh_df = kwh_df.append(missing_inst_df, ignore_index = True)
        #### FILL MISSING KWH DATA ##################
        inst_group = kwh_df.groupby(kwh_df.inst)
        inst_group_size = inst_group.size()
        incomplete_group = list(inst_group_size[inst_group_size != 24].index)
        missing_kwh_df = pandas.DataFrame()
        for inst in incomplete_group:
            inst_df = inst_group.get_group(inst)
            inst_dates = inst_df.date.unique()
            missing_dates = [x for x in all_dates if x not in inst_dates]
            fill_kwh = pandas.DataFrame()
            fill_kwh['date'] = missing_dates
            fill_kwh['inst'] = inst
            missing_kwh_df = missing_kwh_df.append(fill_kwh, ignore_index = True)
        if incomplete_group != []:
            missing_kwh_df['status'] = 1
            missing_kwh_df['kwh'] = missing_kwh_df.apply(fill_hour_mean, axis = 1, df = df)
            missing_kwh_df = missing_kwh_df[['inst', 'date', 'kwh', 'status']]
            kwh_df = kwh_df.append(missing_kwh_df, ignore_index = True)
        #### WRITE TO DATABASE ######################
        kwh_df = kwh_df.sort_values(by = ['date', 'inst'])
        kwh_df.to_sql(name='data', con=sqlengine, if_exists = 'append', index=False)
        update_message_reward(sqlengine)
        message_string = "DATABASE UPDATED SUCCESSFULLY WITH {0} DATA".format(file_date)
        return_message = {"msg": message_string}
    else:
        return_message = {"msg": "DATABASE ALREADY CONTAINS LATEST DATA!!"}
    return return_message


# HELPERS

#### DATA FRAME TRANSFORM FUNCTIONS #########
def fill_hour_mean(row, df):
    inst = row['inst']
    hour = row['date'].hour
    kwh_mean = df.loc[((df.inst == inst) & (df.date.dt.hour == hour)), 'kwh'].mean()
    return kwh_mean