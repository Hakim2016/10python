import time
import json
import re
import requests
import execjs
import rsa
import base64

js_path = 'login.js'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
           }

# 全局的session
session = requests.session()
session.get('https://pan.baidu.com', headers=headers)

def output_html(cntnt, name):
    path1 = '../others/'
    path2 = './others/'
    try:
        with open(path1 + name, 'w', encoding='utf-8') as f:
            f.write(cntnt)
    except:
        with open(path2 + name, 'w', encoding='utf-8') as f:
            f.write(cntnt)

def _get_runntime():
    """
    :param path: 加密js的路径,注意js中不要使用中文！估计是pyexecjs处理中文还有一些问题
    :return: 编译后的js环境，不清楚pyexecjs这个库的用法的请在github上查看相关文档
    """
    phantom = execjs.get()  # 这里必须为phantomjs设置环境变量，否则可以写phantomjs的具体路径
    with open(js_path, 'r') as f:
        source = f.read()
    return phantom.compile(source)


def get_gid():
    return _get_runntime().call('getGid')


def get_callback():
    return _get_runntime().call('getCallback')


def _get_curtime():
    return int(time.time()*1000)


# 抓包也不是百分百可靠啊,这里?getapi一定要挨着https://passport.baidu.com/v2/api/写，才会到正确的路由
def get_token(gid, callback):
    cur_time = _get_curtime()
    get_data = {
        'tpl': 'netdisk',
        'subpro': 'netdisk_web',
        'apiver': 'v3',
        'tt': cur_time,
        'class': 'login',
        'gid': gid,
        'logintype': 'basicLogin',
        'callback': callback
    }
    headers.update(dict(Referer='http://pan.baidu.com/', Accept='*/*', Connection='keep-alive', Host='passport.baidu.com'))
    resp = session.get(url='https://passport.baidu.com/v2/api/?getapi', params=get_data, headers=headers)
    if resp.status_code == 200 and callback in resp.text:
        # 如果json字符串中带有单引号，会解析出错，只有统一成双引号才可以正确的解析
        #data = eval(re.search(r'.*?\((.*)\)', resp.text).group(1))
        data = json.loads(re.search(r'.*?\((.*)\)', resp.text).group(1).replace("'", '"'))
        print(resp.text)
        print(data)
        return data.get('data').get('token')
    else:
        print('获取token失败')
        return None


def get_rsa_key(token, gid, callback):
    cur_time = _get_curtime()
    get_data = {
        'token': token,
        'tpl': 'netdisk',
        'subpro': 'netdisk_web',
        'apiver': 'v3',
        'tt': cur_time,
        'gid': gid,
        'callback': callback,
    }
    resp = session.get(url='https://passport.baidu.com/v2/getpublickey', headers=headers, params=get_data)
    if resp.status_code == 200 and callback in resp.text:
        data = json.loads(re.search(r'.*?\((.*)\)', resp.text).group(1).replace("'", '"'))
        return data.get('pubkey'), data.get('key')
    else:
        print('获取rsa key失败')
        return None


def encript_password(password, pubkey):
    pub = rsa.PublicKey.load_pkcs1_openssl_pem(pubkey.encode('utf-8'))
    encript_passwd = rsa.encrypt(password.encode('utf-8'), pub)
    return base64.b64encode(encript_passwd).decode('utf-8')


def login(token, gid, callback, rsakey, username, password):
    print('callback = ' + callback)
    post_data = {
        'staticpage': 'http://pan.baidu.com/res/static/thirdparty/pass_v3_jump.html',
        'charset': 'utf-8',
        'token': token,
        'tpl': 'netdisk',
        'subpro': 'netdisk_web',
        'apiver': 'v3',
        'tt': _get_curtime(),
        'codestring': '',
        'safeflg': 0,
        'u': 'http://pan.baidu.com/disk/home',
        'isPhone': '',
        'detect': 1,
        'gid': gid,
        'quick_user': 0,
        'logintype': 'basicLogin',
        'logLoginType': 'pc_loginBasic',
        'idc': '',
        'loginmerge': 'true',
        'foreignusername': '',
        'username': username,
        'password': password,
        'mem_pass': 'on',
        # 返回的key
        'rsakey': rsakey,
        'crypttype': 12,
        'ppui_logintime': 33554,
        'countrycode': '',
        'dv': 'MDExAAoASAALAzYAJAAAAF00AAgCACCGhRkY8fHxh3gWcwdjCnkSTT1cL1wDbwBnDmA_WTZEKQwCAB-J6enp6dbfi8qEw5HQncKdzZ7OkaX6pdCjxrT6m_aTBwIABJGRkZEMAgAfievr6-vXPGgpZyByM34hfi59LXJGGUYzQCVXGXgVcAwCAB-J6urq6tb8qOmn4LLzvuG-7r3tsobZhvOA5ZfZuNWwCAIAIYmNGxo8PDwK-Kzto-S297rluuq56baC3YL3hOGT3bzRtA0CAB2Rkafn_6vqpOOx8L3ive2-7rGF2oXwg-aU2rvWswgCAAmRk0RGX19fbvAHAgAEkZGRkQkCABSRkkBCbGxsbGxDJSQnhYVpaT09KQgCAAmRlQkImZmZtb8HAgAEkZGRkQYCACiRkZEyMjIyMjIyN7i4uLsuLi4ri4uLiAwMDAmpqamq9vb281NTU1GWFwIAGJCU5ub1mrbYg9Oj_tK82a6O4LvKuufLpRYCACOzx6ycsoO2hLeFsoqyhbWEsYW0g7GDsoe3gLeAuY-4gbGFvAQCAAaTk5GQpJEFAgAEkZGRnQECAAaRk5ODju4VAgAIkZGQz8FtfgcQAgABkRMCABqRh4eH75vvn-zW-damx6mH5YTtifzSsd6znAcCAASRkZGRCQIAEpeSBQT8_Pz8_OGgoM203KjFqQcCAASRkZGRCQIAEpeSCQpOTk5OTmgoKEU8VCBNIQ0CAAWRkb7Kyg0CAAWRkb56egkCACSJjamokZGRkZGnkJDEhcuM3p_SjdKC0YHe6rXqn-yJ-7XUudwMAgAfiejo6OjTkcWEyo3fntOM04PQgN_rtOue7Yj6tNW43QcCAASRkZGRBwIABJGRkZEMAgAfie7u7u7TKX08cjVnJms0aztoOGdTDFMmVTBCDG0AZQ0CAB2RkdiNlcGAzonbmteI14fUhNvvsO-a6Yz-sNG82Q0CAB2Rkdixqf288rXnpuu067vouOfTjNOjwrHCtdqozAgCACOLj4yNDg4OcRhMDUMEVhdaBVoKWQlWYj1iFHEDagx1Nlk9WAkCACaLiGFgFhYWFhaW-Pis7aPktve65brquem2gt2C9JHjiuyV1rnduA',
        'callback': 'parent.'+callback
    #     bd__cbs__a59usm
    #     bd__pcbs__kw7m3d
    }
    # pan_url = 'https://pan.baidu.com/res/static/thirdparty/pass_v3_jump.html'
    pan_url = 'https://passport.baidu.com/v2/api/?login'
    # resp = session.post(url='https://passport.baidu.com/v2/api/?login', data=post_data, headers=headers)
    resp = session.post(url=pan_url, data=post_data, headers=headers)
    resp.encoding = 'utf-8'
    output_html(resp.text, 'login_baidussssssss.html')
    if 'err_no=0' in resp.text:
        print('登录成功')
        print(resp.text)
        # pan_first_url = 'https://pan.baidu.com/disk/home?errno=0&errmsg=Auth%20Login%20Sucess&&bduss=&ssnerror=0#list/path=%2F&vmode=list'
        pan_first_url = 'https://www.baidu.com'
        # resp = session.post(url='https://passport.baidu.com/v2/api/?login', data=post_data, headers=headers)
        resp = session.post(url=pan_first_url, data=post_data, headers=headers)
        resp.encoding = 'utf-8'
        output_html(resp.text, 'home_pan_baidu.html')
    else:
        print('登录失败')

if __name__ == '__main__':
    print('Input username and password!')
    name = '13270828661'
    passwd = '0513865219hjj'
    # name = input('请输入用户名:\n')
    # passwd = input('请输入密码:\n')

    cur_gid = get_gid()
    print('1 cur_gid = ' + cur_gid)

    cur_callback = get_callback()
    print('2 callback = ' + cur_callback)

    cur_token = get_token(cur_gid, cur_callback)
    print('3 cur_token = ' + cur_token + '\n        via cur_gid & cur_callback')

    cur_pubkey, cur_key = get_rsa_key(cur_token, cur_gid, cur_callback)
    print('4 cur_pubkey = ' + cur_pubkey + '& cur_key = ' + cur_key + '\n       via cur_gid, cur_callback & cur_token')
    encript_pass = encript_password(passwd, cur_pubkey)
    login(cur_token, cur_gid, get_callback().replace('cbs', 'pcbs'), cur_key, name, encript_pass)

    ss = session.get('http://pan.baidu.com/disk/home', headers=headers)
    ss.encoding = 'utf-8'
    output_html(ss.text, 'another_baidu.html')
    # print(ss.text)
