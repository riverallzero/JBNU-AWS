import requests
import pandas as pd
from io import StringIO

import datetime
from pytz import timezone

import os

seoul_timezone = timezone('Asia/Seoul')
today = datetime.datetime.now(seoul_timezone)

year = today.year
month = str(today.month).zfill(2)
day = str(today.day).zfill(2)

url = f'http://203.239.47.148:8080/dspnet.aspx?Site=85&Dev=1&Year={year}&Mon={month}&Day={day}'
raw_data = requests.get(url).text

col_name = ['시간', '온도', '습도', 'x_1', 'x_2', 'x_3', '일사', '풍향', 'x_4', 'x_5',
            'x_6', 'x_7', 'x_8', '픙속(1분 평균)', '강우', '최대순간풍속', '배터리전압']
df = pd.read_csv(StringIO(raw_data), header=None, delimiter=',', names=col_name, index_col=False)

exclude_list = []
for name in df.columns:
    for field in ['x']:
        if name.startswith(field):
            exclude_list.append(name)

df.drop(exclude_list, axis=1, inplace=True)

df_ts = df.tail(1)

api_key = os.environ.get('WRITE_KEY')

field_1 = df_ts['온도'].values[0]
field_2 = df_ts['습도'].values[0]
field_3 = df_ts['일사'].values[0]
field_4 = df_ts['픙속(1분 평균)'].values[0]
field_5 = df_ts['강우'].values[0]

thingspeak_url = f'https://api.thingspeak.com/update?api_key={api_key}&field1={field_1}&field2={field_2}&field3={field_3}&field4={field_4}&field5={field_5}'
response = requests.get(thingspeak_url)
