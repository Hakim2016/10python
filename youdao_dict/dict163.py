from _10python.youdao_dict import dict163_db as yddb
import requests
import re
import http.cookiejar as cookielib
import hashlib
import math
import json
import os
from bs4 import BeautifulSoup

with open('./others/word_first.html', 'r',encoding='utf8') as f:
    first_cnt = f.read()

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
session.cookies = cookielib.LWPCookieJar('../sessions/yd_dict_cookie')
try:
    session.cookies.load('../sessions/yd_dict_cookie')
except:
    print('have not generated the cookies!')
    pass


def login(email, secret):
    print(email)
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
        'password': secret
    }

    login_headers = {
        'Host': 'dict.youdao.com',
        'Origin': 'http://account.youdao.com',
        # 'Referer': 'http://account.youdao.com/login?service=dict&back_url=http%3A%2F%2Fdict.youdao.com%2Fsearch%3Fq%3Dhakim%26tab%3D%23keyfrom%3D%24%7Bkeyfrom%7D',
        'Referer': 'http://account.youdao.com/login?service=dict&back_url=http://dict.youdao.com/wordbook/wordlist%3Fkeyfrom%3Dnull',
        'User-Agent': agent
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Host': 'dict.youdao.com',
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep-alive',
        'User-Agent': agent
    }
    yd_login_url = 'https://logindict.youdao.com/login/acc/login'
    login = session.post(yd_login_url, headers=login_headers, data=postdata)
    session.cookies.save()
    cntnt = login.text
    output_html(cntnt, 'youdao3.html')


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

def get_login_acct():
    wdbk_rsp = session.get(wrdbk_url, headers=headers)
    wdbk_cntn = wdbk_rsp.text
    output_html(wdbk_cntn,'word_page.html')
    acct = re.findall('<span class="un_ml">(.*?)</span>', wdbk_cntn, re.S)[0].strip()
    print(acct)
    session.cookies.save()

def convert_to_json_string_1(data):
    ret = []  # 需要序列化的列表
    for i in data:
        tmp = {'name': i[1], 'value': i[0]}  # 通过data的每一个元素构造一个字典
        ret.append(tmp)
    ret = json.dumps(ret, indent=4, ensure_ascii=False)
    return ret

# deal with the first page, special logic need to consider
def get_first_page():
    each_page = 15
    wrds_url = 'http://dict.youdao.com/wordbook/wordlist?keyfrom=dict2.index'
    wrd_cntnt = session.get(url=wrds_url, headers=headers).text
    wrd_total = int(re.findall('共计 <strong>(.*?)</strong> 个单词', wrd_cntnt)[0])
    cate_list = re.findall('<option value="(.*?)" >', wrd_cntnt)
    tags = get_cate_list(cate_list)
    pages = math.ceil(wrd_total/each_page)

    return (tags, pages, wrd_cntnt)

def get_other_page(page):
    wrd_url = 'http://dict.youdao.com/wordbook/wordlist?p=%d&tags='%page
    wrd_cntnt = session.get(url=wrd_url, headers=headers).text
    return wrd_cntnt

# match the category list with data from database
def get_cate_list(wrdL):
    if len(wrdL) == yddb.yd_cate_cnt():
        print('There is no categories added!')

    wrd_lst = yddb.youdao_lst()
    lst_kv = {}
    for x in wrd_lst:
        lst_kv[x[1]] = x[0]
    return lst_kv

def get_words(wrd_cntnt, tags):
    soup = BeautifulSoup(wrd_cntnt, 'html.parser')
    wrd_lst = str(soup.find('div', attrs={'id':'wordlist'}))

    # 3 key info of a word
    word = re.findall('target="_blank"><strong>(.*?)</strong>', wrd_lst, re.S)
    wrd_time = re.findall('<td width="85px">(.*?)</td>', wrd_lst)
    wrd_tag = re.findall('<div class="tags" title="(.*?)">', wrd_lst)
    #
    # print(str(len(word)) + str(word))
    # print(str(len(wrd_time)) + str(wrd_time))
    # print(str(len(wrd_tag)) + str(wrd_tag))

    for i in range(0, len(word)):
        if wrd_tag[i] == "":
            wrd_tag[i]='无标签'
        # print(str(i+1) + '  |' + word[i].center(20) + '|' + wrd_time[i] + '|' + wrd_tag[i].center(15) + '|' + str(tags[wrd_tag[i]]))
        yddb.youdao_add(word[i],wrd_time[i],tags[wrd_tag[i].lower()])

if __name__ == '__main__':
    email = '13270828661@163.com'
    psswd = '099cd4de374049a3cb5738f7e751e527'
    login(email, psswd)
    get_login_acct()

    (tags, pages, wrd_cntnt) = get_first_page()
    print(tags)
    for i in range(int(pages)):
        print('Dealing with page ' + str(i+1) + '/'+ str(pages) +' now!')
        if i != 0:
            wrd_cntnt = get_other_page(i)
        else:
            pass
        get_words(wrd_cntnt,tags)