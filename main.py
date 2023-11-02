import requests
import pandas as pd
from io import StringIO

import datetime
from pytz import timezone

import os


def update_data():
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

    write_api_key = os.environ.get('WRITE_KEY')

    field_1 = df_ts['온도'].values[0]
    field_2 = df_ts['습도'].values[0]
    field_3 = df_ts['일사'].values[0]
    field_4 = df_ts['픙속(1분 평균)'].values[0]
    field_5 = df_ts['강우'].values[0]

    thingspeak_url = f'https://api.thingspeak.com/update?api_key={write_api_key}&field1={field_1}&field2={field_2}&field3={field_3}&field4={field_4}&field5={field_5}'
    requests.get(thingspeak_url)


def read_data():
    read_api_key = os.environ.get('READ_KEY')
    channel_id = '2328517'
    result_num = 1
    thingspeak_url = f'https://api.thingspeak.com/channels/{channel_id}/feeds.csv?api_key={read_api_key}&results={result_num}'
    response = requests.get(thingspeak_url)

    df = pd.read_csv(StringIO(response.text), header=None,
                     names=['created_at', 'entry_id', '온도', '습도', '일사', '풍속(1분평균)', '강우'], index_col=False)[1:]
    date = df['created_at'].values[0].split(' ')[0]
    df['날짜'] = pd.Timestamp(int(date.split('-')[0]), int(date.split('-')[1]), int(date.split('-')[2]))
    df['시간'] = pd.to_datetime(df['created_at'].values[0].split(' ')[1], format='%H:%M:%S') + pd.Timedelta(hours=9)
    df['시간'] = df['시간'].dt.strftime('%H:%M:%S')
    df['날짜'] = df['날짜'].dt.strftime('%Y-%m-%d')

    df.drop(['created_at', 'entry_id'], axis=1, inplace=True)
    df = df[['날짜', '시간', '온도', '습도', '일사', '풍속(1분평균)', '강우']]

    with open('README.md', 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()

    del lines[2:6]
    lines.insert(2, '## Current Data\n')

    table_lines = []
    table_lines.append('|')
    for column in df.columns:
        table_lines.append(f' {column} |')
    table_lines.append('\n')

    table_lines.append('|')
    for _ in df.columns:
        table_lines.append(' --- |')
    table_lines.append('\n')

    for _, row in df.iterrows():
        table_lines.append('|')
        for value in row:
            table_lines.append(f' {value} |')
        table_lines.append('\n')

    lines[3:3] = table_lines

    with open('README.md', 'w', encoding='utf-8-sig') as f:
        f.writelines(lines)


update_data()
read_data()
