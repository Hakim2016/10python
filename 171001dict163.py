#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Required
- requests (必须)
Info
- author : "xchaoinfo"
- email  : "xchaoinfo@qq.com"
- date   : "2016.2.17"

'''
import requests
import re
import http.cookiejar as cookielib
import hashlib

# youdao_url = 'http://account.youdao.com/login'
# youdao_url = 'http://account.youdao.com/login?service=dict&back_url=http://dict.youdao.com/wordbook/wordlist'
youdao_url = 'https://logindict.youdao.com/login/acc/login'
# 构造 Request headers
agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
headers = {
    'Host': 'shared.ydstatic.com',
    'Origin': 'http://account.youdao.com',
    'Referer': 'http://account.youdao.com/login?service=dict&back_url=http://dict.youdao.com/wordbook/wordlist%3Fkeyfrom%3Dlogin_from_dict2.index',
    'User-Agent': agent
}

# #########Contruct session to connect the server
session = requests.session()
session.cookies = cookielib.LWPCookieJar('./sessions/yd_dict_cookie')
try:
    session.cookies.load('./sessions/yd_dict_cookie')
except:
    print('have not generated the cookies!')
    pass


def login(email, secret):
    secret = encrypt_psswd(secret)
    params = {
        'app': 'web',
        'tp': 'urstoken',
        'cf': 3,
        'fr': 1,
        'ru': 'http://dict.youdao.com/wordbook/wordlist?keyfrom=login_from_dict2.index',
        'product': 'DICT',
        'type': 1,
        'um': 'true'
    }
    postdata = {
        'username': '13270828661@163.com',
        'password': secret,
    }
    login = session.post(youdao_url, data=postdata, headers=headers, params=params)
    session.cookies.save()
    cntnt = login.text
    print(cntnt)

def encrypt_psswd(psswd):
    psswd = psswd.encode('utf-8')
    m = hashlib.md5()
    m.update(psswd)
    return m.hexdigest()

def isLogin():
    # browser private info to verify if we successfully login
    url = 'http://dict.youdao.com/wordbook/wordlist?keyfrom=login_from_dict2.index'
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
        login(email, psswd)
