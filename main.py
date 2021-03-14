#!/usr/bin/env python
# -*- coding: utf-8 -*-

import settings
import datetime
import schedule
import time
import requests
import logging

formatter = '%(levelname)s : %(asctime)s : %(message)s'
logging.basicConfig(filename='logs/log.log', level=logging.DEBUG, format=formatter)

LINE_TOKEN = settings.LINE_TOKEN

casters_master = {
    "hiyama2018": "檜山 沙耶",
    "matsu": "松雪 彩花",
    "ayame": "武藤 彩芽",
    "komaki2018": "駒木 結衣",
    "shirai": "白井 ゆかり",
    "nao": "角田 奈緒子",
    "yuki": "内田 侑希",
    "ailin": "山岸 愛梨",
    "sayane": "江川 清音",
    "izumin": "眞家 泉",
    "takayama": "高山 奈々",
}

def main():
    try:
        response = requests.get('http://smtgvs.weathernews.jp/a/solive_timetable/timetable.json')
        timetables = response.json()
        message = '\n'
        for timetable in timetables:
            if timetable['caster'] != '':
                if timetable['caster'] in casters_master:
                    caster = casters_master[timetable['caster']]
                else:
                    caster = timetable['caster']
            else:
                caster = "公式チャンネル"
            message += "■" + timetable['title'] + "\n"
            message += "　" + timetable['hour'] + "～ （"+ caster+"）\n\n"
        send_line_notify(message)
    except:
        logging.error('error')

def send_line_notify(notification_message):
    line_notify_token = LINE_TOKEN
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': f'{notification_message}'}
    requests.post(line_notify_api, headers = headers, data = data)

if __name__ == "__main__":
    schedule.every().day.at("07:00").do(main)
    while True:
        schedule.run_pending()
        time.sleep(600)

    # main()

