import requests
import re
import http.cookiejar as cookielib
import hashlib
import os

yd_login_url = 'https://logindict.youdao.com/login/acc/login'
# http://dict.youdao.com/wordbook/wordlist
wrdbk_url = 'http://dict.youdao.com/wordbook/wordlist?keyfrom=login_from_dict2.index'
# 构造 Request headers
agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Host': 'dict.youdao.com',
    'Upgrade-Insecure-Requests': '1',
    'Connection': 'keep-alive',
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
    print(secret)
    postdata = {
        'app': 'web',
        'tp': 'urstoken',
        'cf': 3,
        'fr': 1,
        'ru': 'http://dict.youdao.com/search?q=hakim&tab=#keyfrom=${keyfrom}',
        'product': 'DICT',
        'type': 1,
        'um': 'true',
        'username': email,
        'password': secret,
    }

    login_headers = {
        'Host': 'logindict.youdao.com',
        'Origin': 'http://account.youdao.com',
        'Referer': 'http://account.youdao.com/login?service=dict&back_url=http%3A%2F%2Fdict.youdao.com%2Fsearch%3Fq%3Dhakim%26tab%3D%23keyfrom%3D%24%7Bkeyfrom%7D',
        'User-Agent': agent
    }
    login = session.post(yd_login_url, headers=headers, data=postdata)
    session.cookies.save()
    cntnt = login.text
    output_html(cntnt, 'youdao.html')


def output_html(cntnt, name):
    with open('./others/' + name, 'w', encoding='utf-8') as f:
        f.write(cntnt)


def encrypt_psswd(psswd):
    psswd = psswd.encode('utf-8')
    m = hashlib.md5()
    m.update(psswd)
    return m.hexdigest()


def isLogin():
    wrdbk_url2 = 'http://dict.youdao.com/w/eng/hakim/#keyfrom=dict2.index'
    headers['Referer'] = 'http://dict.youdao.com/wordbook/wordlist?keyfrom=login_from_dict2.index'
    # browser private info to verify if we successfully login
    sssn_rsp = session.get(wrdbk_url2, headers=headers)
    output_html(sssn_rsp.text, 'youdao2.html')
    print(sssn_rsp.status_code)
    if sssn_rsp.status_code == 200:
        return True
    else:
        return False


def get_wordbook():
    wdbk_rsp = session.get(wrdbk_url, headers=headers)
    wdbk_cntn = wdbk_rsp.text
    acct = re.findall('<span class="un_ml">(.*?)</span>', wdbk_cntn, re.S)[0].strip()
    print(acct)
    session.cookies.save()

if __name__ == '__main__':
    email = '13270828661@163.com'
    psswd = '099cd4de374049a3cb5738f7e751e527'
    login(email, psswd)
    get_wordbook()

