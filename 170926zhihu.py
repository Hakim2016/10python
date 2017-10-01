import requests
from bs4 import BeautifulSoup
import os, time
import re
import http.cookiejar as cookielib
import json
# from PIL import Image

baseurl = 'https://www.zhihu.com/'
self_url = 'https://www.zhihu.com/settings/profile'
agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
headers = {
    'Host': 'www.zhihu.com',
    'Origin': 'https://www.zhihu.com',
    'Referer': 'https://www.zhihu.com/',
    'User-Agent': agent
}
######构造用于网络请求的session
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='sessions/zhihu_cookie')
try:
    session.cookies.load(ignore_discard=True)
except:
    pass



def captchaZhihu():
    ###### Get Captcha img
    ###### 默认验证码是存在的
    # /captcha.gif?r=1506403581410&type=login&lang=cn
    # get random time
    randomtime = str(int(time.time() * 1000))
    captcha_url = baseurl + 'captcha.gif?r=' + randomtime + '&type=login'
    # captcha_url = baseurl + 'captcha.gif?r='+randomtime+'&type=login&lang=en'
    # request for image, request header is needed
    # cap_ss = session.get(url=captcha_url, headers=headers)
    cap_ss = session.get(captcha_url, headers=headers)

    with open('zhihu_captcha_test.png', 'wb') as f:
        f.write(cap_ss.content)
        f.close()

    os.startfile('zhihu_captcha_test.png')

    # Captcha varies from different language environment
    captcha = input('please input the captcha according to this image!\n')
    print('This is what you input just now : ' + captcha)
    return captcha

def loginZhihu(acct, psswd):
    xsrf = getXsrf()
    post_data = {
        '_xsrf': xsrf,
        'password': psswd,
        # 'captcha_type': 'en',
        # 'email': email
    }
    headers['X-Requested-With'] = 'XMLHttpRequest'
    headers['X-Xsrftoken'] = xsrf

    # how to login
    if re.match('^1\d{10}$', acct):
        print('cellphone number login!')
        login_post = 'https://www.zhihu.com/login/phone_num'
        post_data['phone_num'] = acct
    else:
        if '@' in acct:
            print('login via email!')
            login_post = 'https://www.zhihu.com/login/email'
            post_data['email'] = acct
        else:
            print('There exists something wrong with your account, please check!')
            return

    # try to login without captcha
    login_rsp = session.post(url=login_post, data=post_data, headers=headers)
    json_rsp = login_rsp.json()

    if json_rsp['r'] == 1:
        # captcha is needed
        post_data['captcha'] = captchaZhihu()
        login_rsp = session.post(url=login_post, data=post_data, headers=headers)
        json_rsp = login_rsp.json()
        print(json_rsp['msg'])
        session.cookies.save()
        return json_rsp['r'], json_rsp

def getXsrf():
    loginurl = 'https://www.zhihu.com/#signin'
    s = session.get(url=loginurl, headers=headers)
    soup = BeautifulSoup(s.text, 'html.parser')
    xsrf_token = soup.find('input', attrs={'name': '_xsrf'}).get('value')
    return xsrf_token

def isLogin():
    # browser private info to verify if we successfully login
    url = 'https://www.zhihu.com/settings/profile'
    login_code = session.get(url, headers=headers, allow_redirects=False).status_code
    print(login_code)
    if login_code == 200:
        return True
    else:
        return False

def get_self_code():
    # cookie already in hand!
    personal_code_reg = re.compile('name="url_token" id="url_token" value="(.*?)" required>')
    self_html = session.get(url=self_url, headers=headers, allow_redirects=False)
    # print(self_html.text)
    personal_code = personal_code_reg.findall(self_html.text, re.S)[0]
    print(personal_code)
    return personal_code

def get_personal_info(self_code):
    personal_info_base = 'https://www.zhihu.com/people/' + self_code + '/'
    activities_url = personal_info_base + 'activities/'
    # urls related to personal infomation
    following_url = personal_info_base + 'following/'
    followers_url = personal_info_base + 'followers/'
    following_columns_url = following_url + 'columns/'
    following_topics_url = following_url + 'topics/'
    following_questions_url = following_url + 'questions/'
    following_collections_url = following_url + 'collections/'

    print(activities_url)
    act_cont = session.get(url=activities_url, headers=headers)
    follows = re.findall('<div class="NumberBoard-name">(.*?)</div><div class="NumberBoard-value">(.*?)</div>', act_cont.text)
    concerns = re.findall('<span class="Profile-lightItemName">(.*?)</span><span class="Profile-lightItemValue">(.*?)</span>', act_cont.text,re.S)

# 1506837354
# 1504206499
    after_id = int(time.time())
    per_post_data = {
        'limit':'20',
        'after_id':after_id,
        'desktop':'True'
    }

    '''
    headers = {
    'Host': 'www.zhihu.com',
    'Origin': 'https://www.zhihu.com',
    'Referer': 'https://www.zhihu.com/',
    'User-Agent': agent
}


https://www.zhihu.com/people/ke-ren-33-46/activities
https://www.zhihu.com/people/ke-ren-33-46/activities/

accept:application/json, text/plain, */*
    '''
    headers['accept'] = 'application/json, text/plain, */*'
    headers['Referer'] = activities_url
    headers['authorization'] = 'Bearer Mi4xelhWdkFBQUFBQUFBQUVJR0xFczREQmNBQUFCaEFsVk54TFAwV1FDTzd0TXlTN2xPaTNTZ2QzWEVOTXhBZzZ1UUZR|1506617028|5ef624575e9eb3d8f2f56def8af0d3f7e554273e'
    headers['x-api-version'] = '3.0.40'
    headers['x-udid'] = 'AABCBixLOAyPTvfzgvHdLgczK-8UpO-HanY='
    # 'x-api-version':'3.0.40'
# x-udid:AABCBixLOAyPTvfzgvHdLgczK-8UpO-HanY=

    json_url = 'https://www.zhihu.com/api/v4/members/ke-ren-33-46/activities'

    print(headers)
    personal_jsn = session.get(url=json_url, headers=headers,data= per_post_data)
    print(personal_jsn)
    # print(json_str)
    # following_cnt = follows[0][1]
    # followers_cnt = follows[1][1]

    # topics_cnt = concerns[0][1]
    # columns_cnt = concerns[1][1]
    # questions_cnt = concerns[2][1]
    # collections_cnt = concerns[3][1]
    print(follows)
    print(concerns)
    # print(act_cont.json())

if __name__ == '__main__':
    if isLogin():
        print('You have already login!')
        self_code = get_self_code()
        get_personal_info(self_code)

    else:
        email = input('please input your account!\n')
        psswd = input('please input your password!\n')

        (r, json) = loginZhihu(email,psswd)
        print(r)
        print(json)