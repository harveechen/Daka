from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
import json
import time
import os
from datetime import datetime, timezone, timedelta
from schedule import every, repeat, run_pending

service = 'http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/getApplyInfoList.do'
url = f'https://authserver.nju.edu.cn/authserver/login?service={service}'
base_url = 'http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/saveApplyInfos.do'

username = os.environ['EHALL_USERNAME']  # ehall username
password = os.environ['EHALL_PASSWARD']  # ehall password
loc = os.environ['DAKA_ADDRESS']  # address


def get_wid_and_cookies():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--headless')

    with webdriver.Remote(command_executor="http://localhost:3000/webdriver",
                          options=chrome_options) as b:
        b.get(url)
        b.find_element(By.ID, 'username').send_keys(username)
        b.find_element(By.ID, 'password').send_keys(password)
        b.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        content = b.find_element(By.TAG_NAME, "pre")
        res = json.loads(content.text)
        cookies = ';'.join(
            [item['name'] + '=' + item['value'] for item in b.get_cookies()])

    time_formt = "%b %d, %Y %H:%M:%S %p"
    data = sorted(res['data'],
                  key=lambda x: time.strptime(x['CJSJ'], time_formt),
                  reverse=True)
    wid = data[0]['WID']

    return wid, cookies

def daka():
    wid, cookies = get_wid_and_cookies()
    payload = {
        'WID': wid,
        'CURR_LOCATION': loc,
        'IS_TWZC': 1,
        'IS_HAS_JKQK': 1,
        'JRSKMYS': 1,
        'JZRJRSKMYS': 1
    }

    headers = {'Cookie': cookies}
    resp = requests.request("GET", base_url, params=payload, headers=headers)
    resp_json = json.loads(resp.text)

    return resp_json['msg']

def get_time_str():
    utc = timezone.utc
    utc_time = datetime.utcnow().replace(tzinfo=utc)
    beijing = timezone(timedelta(hours=8))

    return utc_time.astimezone(beijing)

@repeat(every().day.at('10:30'))
# @repeat(every(2).seconds)
def job():
    msg = daka()
    timestamp = get_time_str()
    print(f'{timestamp}: {msg}')

if __name__ == '__main__':
    while True:
        run_pending()
