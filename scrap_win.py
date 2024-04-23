from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
import os

import json
import requests

corp_id = 'wwxxxxxxx'
corp_secret = 'R3Jxxxxxxx'
agent_id = '100xxxx'

def get_access_token(corp_id, corp_secret):
    resp = requests.get(f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corp_id}&corpsecret={corp_secret}')
    js = json.loads(resp.text)
    print(js)
    if js["errcode"] == 0:
        access_token = js["access_token"]
        expires_in = js["expires_in"]
        return access_token, expires_in

def wechat_push_text(agent_id, access_token, message):
    data = {
        "touser": "@all",
        "msgtype": 'text',
        "agentid": agent_id,
        "text": {
            "content": message
        },
        "safe": 0,
        "enable_id_trans": 0,
        "enable_duplicate_check": 0,
        "duplicate_check_interval": 1800
    }
    resp = requests.post(f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}', json=data)
    js = json.loads(resp.text)
    print(js)
    if js["errcode"] == 0:
        return js


geckodriver_path = Service('D:/00_Working/03_py/shiny/01_test/geckodriver.exe')

options = Options()
# 无头模式
options.add_argument("--headless") 

options.set_preference("browser.tabs.warnOnClose", False)
options.binary_location = r'D:\Software\Mozilla Firefox x64\firefox.exe'
driver = webdriver.Firefox(service=geckodriver_path, options=options)
driver.get("http://www.fangdi.com.cn/old_house/old_house.html")


wait = WebDriverWait(driver, 30, poll_frequency=1)
element = wait.until(EC.element_to_be_clickable((By.ID, "z_sell_num_p")))

num = element.get_attribute('textContent')
current_dateTime = datetime.now()
date_time = current_dateTime.strftime("%m/%d/%Y, %H:%M:%S")
print(date_time)
print("昨日二手房成交套数：" + num)
access_token, expires_in = get_access_token(corp_id, corp_secret)
wechat_push_text(agent_id=agent_id, access_token=access_token, message='脚本运行时间：' + date_time + '\n昨日二手房成交套数：' + num + '\n                                 - 小道无知')
# quit page
driver.quit()

with open('D:/00_Working/ZZ/20240422/dailyout.txt', 'a') as f: 
    f.write(date_time + '\t' + num + '\n')
