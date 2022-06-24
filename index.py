import time
import requests
import json
import datetime
from bs4 import BeautifulSoup
# import os
# os.system('cls')
# by jeblove
requests.packages.urllib3.disable_warnings()

'''
cd src
pip3 install -r requirements.txt -t ./ 

pip3 install bs4
pip3 install beautifulsoup4
pip3 install requests

'''

username = ''
password = ''
pushkey = ''
'''
username: 账号
password: 密码
pushkey: pushdeer消息推送key ,不需要推送则留空 ,详细了解
https://github.com/easychen/pushdeer

crontab建议
0 12,20 * * *
'''

headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36',
    "Referer": "http://rz2.gdsdxy.edu.cn/zfca/login?yhlx=student&login=0122579031373493749&url="
}
# "Referer": "http://rz2.gdsdxy.edu.cn/zfca/login?yhlx=student&login=0122579031373493749&url="

loginURL = 'http://rz2.gdsdxy.edu.cn/zfca/login?yhlx=student&login=0122579031373493749&url='
signInURL = 'http://dgsx.gdsdxy.cn/a/statistics/signin/save'

s = requests.session()
s.headers = headers

def get_beijin_time():
    try:
        urlBeijingT = 'https://beijing-time.org/'
        request_result = requests.get(url=urlBeijingT)
        if request_result.status_code == 200:
            headers = request_result.headers
            net_date = headers.get("date")
            gmt_time = time.strptime(net_date[5:25], "%d %b %Y %H:%M:%S")
            bj_timestamp = int(time.mktime(gmt_time) + 8 * 60 * 60)
            return datetime.datetime.fromtimestamp(bj_timestamp)
    except Exception as exc:
        return datetime.datetime.now()

def push(pushkey,signFlagS):
    # data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) # 本机时间
    data = get_beijin_time().strftime("%Y-%m-%d %H:%M:%S")
    print(data)

    text = signFlagS

    url = 'https://api2.pushdeer.com/message/push?pushkey='+pushkey+'&text='+data+'%0A'+text

    x=s.post(url,verify=False)
    print('消息推送成功')

def signFunc(username,password):

    r = s.get(url=loginURL)
    soup = BeautifulSoup(r.text,'html.parser')
    for t in soup.find_all('input',attrs={'name':'lt'}):
        lt = t.get('value')
    print(lt)

    data = {
        "useValidateCode" : 0,
        "isremenberme" : 1,
        "ip" : "",
        "username" : username,
        "password" : password,
        "losetime" : 30,
        "lt" : lt,
        "_eventId" : "submit",
        "submit1" : ""
    }

    r = s.post(url=loginURL,data=data)
    # print(r.json())
    # print(r.text)
    print(r.headers['Content-Type'])
    # print(r.encoding)
    # print(r.cookies)
    print(r.status_code)
    print(r.url)
    if(r.url == 'http://dgsx.gdsdxy.cn/a' and r.status_code == 200):
        signFlagS = '顶岗实习%0A登录成功'
        
        try:
            signWeb = s.get(url=signInURL)
            print('signWeburl=',signWeb.url)
            print('signWeburl=',signWeb.status_code)
            print(signWeb.json())
            state = signWeb.json().get('success')
            print(state)
            if(state==False):
                signFlagS += '%0A今天已经签到了'
            else:
                signFlagS += '%0A签到成功'
        except:
            print('出现错误，签到失败')
            signFlagS += '%0A签到失败，请稍后再试'
        
    else:
        signFlagS = '登录失败，可能是页面无法访问，请稍后再试'
    return signFlagS


def main_handler(*args,**kwargs):
    result = signFunc(username,password)
    print(result)
    print('脚本执行完毕')
    if(len(pushkey)!=0):
        push(pushkey,result)
    print('by jeblove')

if __name__=='__main__':
    main_handler()