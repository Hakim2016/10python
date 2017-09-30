import requests
from bs4 import BeautifulSoup
import os, time
import re
import http.cookiejar as cookielib
# from PIL import Image

baseurl = 'https://www.zhihu.com/'
agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
headers = {
    'Host': 'www.zhihu.com',
    'Origin': 'https://www.zhihu.com',
    'Referer': 'https://www.zhihu.com/',
    'User-Agent': agent
}
######构造用于网络请求的session
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')
session.cookies.load(ignore_discard=True)

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

if __name__ == '__main__':
    if isLogin():
        print('You have already login!')
    else:
        email = input('please input your account!\n')
        psswd = input('please input your password!\n')

        (r, json) = loginZhihu(email,psswd)
        print(r)
        print(json)