#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import schedule
import time
import requests
import logging
import yaml
import re

formatter = '%(levelname)s : %(asctime)s : %(message)s'
logging.basicConfig(filename='logs/log.log', level=logging.DEBUG, format=formatter)

def main():
    try:
        response = requests.get('http://smtgvs.weathernews.jp/a/solive_timetable/timetable.json')
        timetables = response.json()
        message = '\n'
        for timetable in timetables:
            if timetable['caster'] != '':
                if timetable['caster'] in config['announcer']:
                    caster = config['announcer'][timetable['caster']]['name']
                else:
                    caster = timetable['caster']
            else:
                caster = "公式チャンネル"
            message += "■" + timetable['title'].replace("ウェザーニュース", "") + "\n"
            message += "　" + timetable['hour'] + "～ （"+ caster+"）\n\n"

        message = re.sub('\n\n$', '', message)
        send_line_notify(message)
    except:
        logging.error('error')

def send_line_notify(notification_message):
    line_notify_token = config['line_token']
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': f'{notification_message}'}
    requests.post(line_notify_api, headers = headers, data = data)

if __name__ == "__main__":
    with open('config.yaml', 'r', encoding='UTF-8') as file:
        config = yaml.safe_load(file)

    for notification_time in config['notification_time']:
        schedule.every().day.at(notification_time).do(main)

    while True:
        schedule.run_pending()
        time.sleep(30)

    # main()

