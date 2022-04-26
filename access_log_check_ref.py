#!/usr/bin/python3

import sys
import subprocess
import smtplib
from datetime import datetime
import json
import requests
from dotenv import dotenv_values

envs = dotenv_values(".env")

def telegram(msg):
    requests.post('https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(
        envs['TELEGRAM_BOT_TOKEN'], envs['TELEGRAM_CHAT_ID'], msg
        ))

def send_notify(msgs):
    message = '\n'.join(msgs)

    self.telegram(message)

if __name__ == '__main__':
    files = {
        'domain': {'path': '/var/log/nginx/access.log', 'group': 't4a', 'domain': 'domain.com', 'full': True, 'ig': 'domain.com'},
        # add more domain here
    }

    contents = []

    for site, logs in files.items():
        filelog = logs['path']
        telegroup = logs['group']
        domain = logs['domain']

        subprocess.call('./access_log_check_ref {} {} 2>&1'.format(filelog, domain), shell=True)

        json_file='/tmp/access_log_check_ref_json_{}'.format(site)

        data = {}
        try:
            with open(json_file) as f:
                data = json.loads(f.read())
        except:
            pass

        save_data = {}

        msgs = []
        tmplist = []
        total = 0
        last = 0
        try:
            with open('/tmp/access_ref_{}'.format(domain)) as f:
                lines = f.readlines()
                for l in lines:
                    l = l.replace('\n', '').strip()
                    arr = l.split(' ')

                    k = int(arr[0])
                    total = total + k
                    v = arr[1]
                    k_increase = 0
                    if v in data.keys():
                        k_increase = k - int(data[v])

                    if k_increase == 0 and False:
                        total = total - k
                        continue

                    save_data[v] = k

                    last = last + k_increase

                    total_char = 30
                    total_char1 = 5
                    remain_whitespace = total_char - len(v)
                    remain_whitespace1 = total_char1 - len(str(k_increase))

                    if(v == logs['ig']):
                        continue

                    l = '+{}{}{}{}{}'.format(k_increase, remain_whitespace1*' ', v, remain_whitespace*' ', k)
                    if k_increase > 0 or logs['full']:
                        msgs.append(l)
                    else:
                        tmplist.append(l)
                    print(l)
        except:
            print('no log', domain)

        with open(json_file, 'w') as f:
            f.write(json.dumps(save_data))

        contents = []
        msgs.append('last: {}'.format(last))
        msgs.append('total: {}'.format(total))
        if len(msgs) > 0:
            contents.append('[{}] Referal #ffffffffffffffffffffffffffffffffffff\n'.format(site[0:8])+'\n'.join(msgs))

        send_notify(contents)