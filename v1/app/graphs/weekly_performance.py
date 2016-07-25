import datetime
import pandas

def weekly_performance(instance_num, sqlengine):
    #### FETCH 14 DAYS DATA OF THE USER #########
    last_day = (datetime.date.today() - datetime.timedelta(days = 3))
    last = datetime.datetime.combine(last_day, datetime.time(23,0,0))
    first_day = last_day - datetime.timedelta(days = 13)
    first = datetime.datetime.combine(first_day, datetime.time(0,0,0))
    query = "SELECT date(date), avg(kwh)*24 AS kwh FROM data WHERE inst = {0} AND date BETWEEN \'{1}\' AND \'{2}\' GROUP BY date(date) ORDER BY date(date);".format(instance_num, first, last)
    user_df = pandas.read_sql_query(query,con=sqlengine)
    ## (user_df-kwh-column-key) -> (whole-number)
    ## Given the day, returns users consumption from the last 14 days data & exception handling for no data.
    def kwh_value(x):
        try:
            return int(round(user_df.kwh[x]))
        except KeyError:
            return 0

    ## (user_df-kwh-column-key) -> (whole-number)
    ## Given the day, returns change in users consumption compared to same day of last week & exception handling for no data.
    def last_week_diff(x):
        try:
            return int(round(user_df.kwh[x + 7])) - int(round(user_df.kwh[x]))
        except KeyError, e:
            return 0

    ## Lists for user's consumption for last 7 days, user's change in daily consumption since the week before, and dates of last 7 days in YYYY-MM-DD
    user_day = list(map(kwh_value, range(7,14)))
    user_change = list(map(last_week_diff, range(0,7)))
    day = list(map(lambda x: (datetime.date.today() - datetime.timedelta(days = x)).strftime(format = '%Y-%m-%d'), list(reversed(range(3,10)))))

    #### FETCH 7 DAY DATA OF SIMILAR HOMES ######
    last_day = (datetime.date.today() - datetime.timedelta(days = 3))
    last = datetime.datetime.combine(last_day, datetime.time(23,0,0))
    first_day = last_day - datetime.timedelta(days = 6)
    first = datetime.datetime.combine(first_day, datetime.time(0,0,0))
    query = 'SELECT persons, hsize, htype FROM attr WHERE inst = {0};'.format(instance_num)
    details_df = pandas.read_sql_query(query,con=sqlengine)
    details = list(details_df.iloc[0])
    query = 'SELECT inst FROM attr WHERE persons = \'{0}\' AND hsize = \'{1}\' AND htype = \'{2}\';'.format(details[0], details[1], details[2].encode('utf8'))
    inst_df = pandas.read_sql_query(query,con=sqlengine)
    inst_list = list(inst_df['inst'])
    inst_list_query = str(tuple(inst_list)).rstrip(',)') + ')'
    query = "SELECT date(date), avg(kwh)*24 AS kwh FROM data WHERE inst IN {0} AND date BETWEEN \'{1}\' AND \'{2}\' GROUP BY date(date);".format(inst_list_query, first, last)
    others_df = pandas.read_sql_query(query,con=sqlengine)

    ## (user_df-kwh-column-key) -> (whole-number)
    ## Given the day, returns others' avg consumption from the last 14 days data & exception handling for no data.
    def others_value(x):
        try:
            return int(round(others_df.kwh[x]))
        except KeyError:
            return 0

    others_day = list(map(others_value, range(0,7)))

    #### 7 DAY GRAPH DATA #######################
    performanceData = {
    "data": [
    { "data": { "x": others_day[0], "y": day[0] }, "color": "#b3b3b3" },
    { "data": { "x": user_day[0], "y": day[0] }, "color": "#8BC34A", "change": {"x": user_day[0] - others_day[0], "color": "#ff3374" } },
    { "data": { "x": others_day[1], "y": day[1] }, "color": "#b3b3b3" },
    { "data": { "x": user_day[1], "y": day[1] }, "color": "#8BC34A", "change": {"x": user_day[1] - others_day[1], "color": "#ff3374" } },
    { "data": { "x": others_day[2], "y": day[2] }, "color": "#b3b3b3" },
    { "data": { "x": user_day[2], "y": day[2] }, "color": "#8BC34A", "change": {"x": user_day[2] - others_day[2], "color": "#ff3374" } },
    { "data": { "x": others_day[3], "y": day[3] }, "color": "#b3b3b3" },
    { "data": { "x": user_day[3], "y": day[3] }, "color": "#8BC34A", "change": {"x": user_day[3] - others_day[3], "color": "#ff3374" } },
    { "data": { "x": others_day[4], "y": day[4] }, "color": "#b3b3b3" },
    { "data": { "x": user_day[4], "y": day[4] }, "color": "#8BC34A", "change": {"x": user_day[4] - others_day[4], "color": "#ff3374" } },
    { "data": { "x": others_day[5], "y": day[5] }, "color": "#b3b3b3" },
    { "data": { "x": user_day[5], "y": day[5] }, "color": "#8BC34A", "change": {"x": user_day[5] - others_day[5], "color": "#ff3374" } },
    { "data": { "x": others_day[6], "y": day[6] }, "color": "#b3b3b3" },
    { "data": { "x": user_day[6], "y": day[6] }, "color": "#8BC34A", "change": {"x": user_day[6] - others_day[6], "color": "#ff3374" } },
    ],
    "settings": {
        "title": "null",
        "legend": [
            { "title": "Homes like yours", "color": "#b3b3b3"},
            { "title": "Your home", "color": "#8BC34A"},
            { "title": "", "color": "#b3b3b3"},
            { "title": "", "color": "#8BC34A"}
        ],
        "labelFontSize": 12,
        "minValue": 0,
        "maxValue": 15,
        "unit": "(kWh)"
        },
    "graph2": {
        "data": [
        { "data": { "x": user_day[0] - user_change[0], "y": day[0] }, "color": "#b3b3b3" },
        { "data": { "x": user_day[0], "y": day[0] }, "color": "#8BC34A", "change": {"x": user_change[0], "color": "#ff3374" } },
        { "data": { "x": user_day[1] - user_change[1], "y": day[1] }, "color": "#b3b3b3" },
        { "data": { "x": user_day[1], "y": day[1] }, "color": "#8BC34A", "change": {"x": user_change[1], "color": "#ff3374" } },
        { "data": { "x": user_day[2] - user_change[2], "y": day[2] }, "color": "#b3b3b3" },
        { "data": { "x": user_day[2], "y": day[2] }, "color": "#8BC34A", "change": {"x": user_change[2], "color": "#ff3374" } },
        { "data": { "x": user_day[3] - user_change[3], "y": day[3] }, "color": "#b3b3b3" },
        { "data": { "x": user_day[3], "y": day[3] }, "color": "#8BC34A", "change": {"x": user_change[3], "color": "#ff3374" } },
        { "data": { "x": user_day[4] - user_change[4], "y": day[4] }, "color": "#b3b3b3" },
        { "data": { "x": user_day[4], "y": day[4] }, "color": "#8BC34A", "change": {"x": user_change[4], "color": "#ff3374" } },
        { "data": { "x": user_day[5] - user_change[5], "y": day[5] }, "color": "#b3b3b3" },
        { "data": { "x": user_day[5], "y": day[5] }, "color": "#8BC34A", "change": {"x": user_change[5], "color": "#ff3374" } },
        { "data": { "x": user_day[6] - user_change[6], "y": day[6] }, "color": "#b3b3b3" },
        { "data": { "x": user_day[6], "y": day[6] }, "color": "#8BC34A", "change": {"x": user_change[6], "color": "#ff3374" } },
        ],
        "settings": {
            "title": "null",
            "legend": [
                { "title": "Your home last week", "color": "#b3b3b3"},
                { "title": "Your home this week", "color": "#8BC34A"}
            ],
            "labelFontSize": 12,
            "minValue": 0,
            "maxValue": 15,
            "unit": "(kWh)"
            }
    }
    }
    return performanceData