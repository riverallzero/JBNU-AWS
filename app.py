import datetime
from pytz import timezone
import pandas as pd
import requests
import os

from io import StringIO
from tqdm import tqdm
from flask import Flask, render_template

app = Flask(__name__)

seoul_timezone = timezone('Asia/Seoul')
today = datetime.datetime.now(seoul_timezone)
year = today.year
month = str(today.month).zfill(2)
day = str(today.day).zfill(2)

end_date = pd.to_datetime(f'{year}-{month}-{day}', format='%Y-%m-%d')
start_date = end_date + pd.Timedelta(days=-13)

date_range = pd.date_range(start=f'{start_date.year}-{start_date.month}-{start_date.day}',
                           end=f'{end_date.year}-{end_date.month}-{end_date.day}')


def download_aws():
    output_dir = 'data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    df_list = []
    for date in tqdm(date_range):
        year, month, day = date.year, str(date.month).zfill(2), str(date.day).zfill(2)

        url = f'http://203.239.47.148:8080/dspnet.aspx?Site=85&Dev=1&Year={year}&Mon={month}&Day={day}'

        raw_data = requests.get(url).text

        col_name = ['날짜', '온도', '습도', 'x_1', 'x_2', 'x_3', '일사', '풍향', 'x_4', 'x_5',
                    'x_6', 'x_7', 'x_8', '픙속(1분 평균)', '강우', '최대순간풍속', '배터리전압']
        df = pd.read_csv(StringIO(raw_data), header=None, delimiter=',', names=col_name, index_col=False)

        exclude_list = []
        for name in df.columns:
            for field in ['x']:
                if name.startswith(field):
                    exclude_list.append(name)

        df.drop(exclude_list, axis=1, inplace=True)
        df_list.append(df)

    df = pd.concat(df_list)
    df.to_csv(os.path.join(output_dir, f'{start_date.year}{str(start_date.month).zfill(2)}{str(start_date.day).zfill(2)}-{end_date.year}{str(end_date.month).zfill(2)}{str(end_date.day).zfill(2)}.csv'), index=False)


@app.route('/')
def draw_graph():
    df = pd.read_csv(
        f'./data/{start_date.year}{str(start_date.month).zfill(2)}{str(start_date.day).zfill(2)}-{end_date.year}{str(end_date.month).zfill(2)}{str(end_date.day).zfill(2)}.csv')

    days_7 = date_range[6]

    date_list = [date_range[7].strftime('%Y.%m.%d'), date_range[-1].strftime('%Y.%m.%d'), date_range[0].strftime('%Y.%m.%d'), date_range[6].strftime('%Y.%m.%d')]

    df['날짜'] = pd.to_datetime(df['날짜'])
    week_past = df[df['날짜'] < days_7]
    week_now = df[df['날짜'] >= days_7]

    # Feature: temp, humid, rain
    # [min, max, past_mean, now_mean]
    feature_list = []

    for item in ['온도', '습도', '강우', '픙속(1분 평균)']:
        week_past_min = week_past[item].min()
        week_past_max = week_past[item].max()
        week_now_min = week_now[item].min()
        week_now_max = week_now[item].max()

        item_past_mean = week_past[item].mean()
        item_now_mean = week_now[item].mean()

        feature_list.append([week_past_min, week_past_max, week_now_min, week_now_max, item_past_mean, item_now_mean])

    return render_template('index.html', feature_list=feature_list, date_list=date_list)


def main():
    download_aws()
    app.run(debug=True)


if __name__ == '__main__':
    main()
