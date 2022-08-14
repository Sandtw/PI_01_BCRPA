from datetime import datetime
import copy
import requests
import json
import pandas as pd
import numpy as np

def requests_api(api, components, token, last_days = None):
    dic_apis = {}
    for component in components:
        url = api + '/' + component
        response = requests.get(url, headers = _headers)
        dataJson = response.json()
        if last_days:
            dic_apis[component] = pd.DataFrame(dataJson).sort_values(by = 'd').tail(last_days).reset_index(drop = True)
        else:
            dic_apis[component] = pd.DataFrame(dataJson).sort_values(by = 'd')

    return dic_apis

def preprocess_response(dic_apis):
    apis = copy.deepcopy(dic_apis)
    for api in apis:
        df_api = apis[api]
        df_api['date'] = pd.to_datetime(df_api.d)
        df_api['day'] = df_api['date'].dt.day
        df_api['week'] = df_api['date'].dt.week
        df_api['weekday'] = df_api['date'].dt.weekday
        df_api['month'] = df_api['date'].dt.month
        df_api['year'] = df_api['date'].dt.year
        df_api['date-int'] = df_api['date'].apply(datetime.toordinal)
        del df_api['d']


    return apis