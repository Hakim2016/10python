import time
import json
import re
import requests
import execjs
import rsa
import base64
import os
import http.cookiejar as cookielib

js_path = './login.js'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
           }

cookie_path = '../sessions/'

if os.path.exists(cookie_path):
    pass
else:
    print('this path need to create!')
    cookie_path = ''
    # os.makedirs(cookie_path)

# 全局的session
session = requests.session()
session.get('https://pan.baidu.com', headers=headers)
session.cookies = cookielib.LWPCookieJar(cookie_path + 'baidu_pan_cookie')
try:
    session.cookies.load(cookie_path + 'baidu_pan_cookie')
except:
    print('have not generated the cookies!')
    pass

def output_html(cntnt, name):
<<<<<<< HEAD
    name = time.strftime('%Y-%m-%d-%H%M%S',time.localtime(time.time())) + name
    path1 = '../others/'
    path2 = './others/'
=======
    name = time.strftime('%Y-%m-%d-%H%M',time.localtime(time.time())) + name
    path = './others/'
    if os.path.exists(path):
        pass
    else:
        print('this path need to create!')
        os.makedirs(path)

>>>>>>> 208c3b878716403e6a17b08578ae55204b82f727
    try:
        with open(path + name, 'w', encoding='utf-8') as f:
            f.write(cntnt)
    except:
        print('Write error')

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
        print('Please check token json in the token.json')
        output_html(resp.text, 'token.json')
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
        'dv': 'MDExAAoAbwALAzQAIQAAAF00AAgCACqwtLa3qqqq7aH1tPq9767jvOOz4LDv24TbttO-3LnLm_qJ-q3fvs6-26kNAgAdkZGslo7am9WSwIHMk8ycz5_A9Kv0hOWW5ZL9j-sHAgAEkZGRkQkCACSJjZWUk5OTk5OuubntrOKl97b7pPur-Kj3w5zDs9Kh0qXKuNwIAgAJkZWNjAcHBz6hDAIAH4m_v7-_mF4KSwVCEFEcQxxMH08QJHskUSJHNXsadxIHAgAEkZGRkQwCAB-Jvb29vZsseDl3MGIjbjFuPm09YlYJViNQNUcJaAVgBwIABJGRkZEMAgAfibu7u7ufXAhJB0ASUx5BHk4dTRImeSZTIEU3eRh1EAcCAASRkZGRDAIAH4ny8vLy_HMnZihvPXwxbjFhMmI9CVYJfA9qGFY3Wj8HAgAEkZGRkQkCACSJivT0Li4uLi4ub287ejRzIWAtci19Ln4hFUoVYBN2BEorRiMHAgAEkZGRkQYCACiRkZEICAgIVVVVUcHBwcMODg4Lq6urqCwsLCmJiYmK1tbW0nNzc3HmFwIAFJOTj4-A7rX0lciT_ab_kM3lp8bvFgIAI7PHrJyygrqNuoq6iriIsYm-i7-Pu4Oyh7ePt4a3gLKGv4-4BAIABpOTkZCkkQECAAaRk5ODju4FAgAEkZGRnRUCAAiRkZDPg6x08xACAAGREwIAGpGHh4fvm--f7Nb51qbHqYflhO2J_NKx3rOcDQIAHZGRkd7GktOd2ojJhNuE1IfXiLzjvMm6363jgu-KBwIABJGRkZENAgAdkZGD9u66-7XyoOGs86z8r_-glMuU4ZL3hcuqx6IIAgAVnZnw8MjIyN8DbwBnDmBNJUAhRSBSDQIAHZGRse_3o-Ks67n4teq15bbmuY3SjfiL7pzSs967CQIAJImNv79qampqakosLHg5dzBiI24xbj5tPWJWCVYjUDVHCWgFYAwCAB-JsbGxsZlNGVgWUQNCD1APXwxcAzdoN0IxVCZoCWQBDQIAHZGRrJ6G0pPdmsiJxJvElMeXyPyj_In6n-2jwq_KCQIAIoeDm5rMzMzMzIcYGEwNQwRWF1oFWgpZCVZiPWIRZAZrAnY',
        'callback': 'parent.'+ callback
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
        # print(resp.text)
        session.cookies.save()
    else:
        if 'err_no=257' in resp.text:
            # print('Verify code is needed!')
            print('Maybe params dv need to change!')
        print('登录失败')
        
def is_login():
    # headers.update()
    url = 'http://www.baidu.com'
    rsp = session.get(url=url, headers=headers)
    print('check the output html')
    output_html(rsp.text,'baidu_home.html')
    try:
        print('in try excpt')
        username = re.findall('<span class=user-name>(.*?)</span>', rsp.text)[0]
        print('username is ' + username)
    except Exception as e:
        print('Fail to find the username, please contact the producer!')
        return False
    return True

def browse_pan():
    pan_url = 'https://pan.baidu.com/'
    pan_url = 'https://pan.baidu.com/disk/home?errno=0&errmsg=Auth%20Login%20Sucess&&bduss=&ssnerror=0#list/path=%2F&vmode=list'
    pan_url = 'https://pan.baidu.com/disk/home'

    headers.update(dict(Referer='http://pan.baidu.com/', Accept='*/*', Connection='keep-alive', Host='pan.baidu.com'))
    rsp = session.get(url=pan_url, headers=headers)
    rsp.encoding = 'utf-8'
    print('check the output html')
    output_html(rsp.text,'baidu_pan_home.html')

def get_json():
    post_data = {
        'dir': '%2F',
        'bdstoken': '2c1ec15c52758f8bb011a5b6a2c48a18',
        'logid': 'MTUwODQxMzE1NDYyNTAuNTUwMjE5NzA5Mjg2NDY2Mg==',
        'num': '100',
        'order': 'time',
        'desc': '1',
        'clienttype': '0',
        'showempty': '0',
        'web': '1',
        'page': '1',
        'channel': 'chunlei',
        'app_id': '250528'
    }
    # First page
    jsn_url = 'https://pan.baidu.com/api/list?dir=%2F&bdstoken=2c1ec15c52758f8bb011a5b6a2c48a18&logid=MTUwODQxMzE1NDYyNTAuNTUwMjE5NzA5Mjg2NDY2Mg==&num=100&order=time&desc=1&clienttype=0&showempty=0&web=1&page=1&channel=chunlei&web=1&app_id=250528'
    jsn_url = 'https://pan.baidu.com/api/list'
    rsp = session.post(url=jsn_url, headers=headers, data=post_data)
    # print(rsp.text)
    pass

def write2File(result): 
    with open('directories_baidu_pan','w') as f:
        f.write(result)
        f.write('\n')
        f.close()

def getList(path, token):
    payload = {
        'order': 'name',
        'desc': '1',
        'showempty': '0',
        'web': '1',
        'page': '1',
        'num': '100',
        'dir': path,
        't': '0.023670486407354474',
        'bdstoken': token,
        'channel': 'chunlei',  
        'clienttype': '0',
        'web': '1',  
        'app_id': '250528',
        'logid':'MTUwODgxMjcxMzE4ODAuNzI2NjcwNjE1MTQyMjExMw=='
    }
    print(payload)
    # https://pan.baidu.com/api/list
    headers.update(dict(Referer='https://pan.baidu.com/disk/home', Accept='*/*', Connection='keep-alive', Host='pan.baidu.com'))
    path_cnt = session.get("http://pan.baidu.com/api/list", params=payload ,headers=headers)''',verify=False'''
    path_cnt.encoding = 'utf8'
    output_html(path_cnt.text, 'baidu_pan_list.html')
    # print(path_cnt.text)
    # printself.Path.text  
    # mJson = list(json.loads(path_cnt.text)['list'])  
    # for str in mJson:  
    #     if str['isdir'] == 0:  
    #         try:  
    #             printstr['server_filename'].decode('utf-8')  
    #         except:  
    #             printstr['server_filename'].decode('gbk')  
    #         write2File(str['server_filename'])  
    #     elif str['isdir'] == 1:  
    #         try:  
    #             print(str['path']).decode('utf-8')  
    #         except:  
    #             print(str['path']).decode('gbk')  
    #         write2File(str['path'])  
    #         path = str['path'] + '/'  
    #         getList(path) 

def get3Params():
    cur_gid = get_gid()
    print('1 cur_gid = ' + cur_gid)

    cur_callback = get_callback()
    print('2 callback = ' + cur_callback)

    cur_token = get_token(cur_gid, cur_callback)
    print('3 cur_token = ' + cur_token + '\n        via cur_gid & cur_callback')

    return (cur_gid, cur_callback, cur_token)

if __name__ == '__main__':
    if is_login():
        (cur_gid, cur_callback, cur_token) = get3Params()
        print('Cookie load success!')
        getList('/', cur_token)
        pass
    else:
        print('Input username and password!')
        # passwd = '05138xxxxxx'
        name = input('请输入用户名:\n')
        passwd = input('请输入密码:\n')

        (cur_gid, cur_callback, cur_token) = get3Params()

        cur_pubkey, cur_key = get_rsa_key(cur_token, cur_gid, cur_callback)
        print('4 cur_pubkey = ' + cur_pubkey + '& cur_key = ' + cur_key + '\n       via cur_gid, cur_callback & cur_token')
        encript_pass = encript_password(passwd, cur_pubkey)
        login(cur_token, cur_gid, get_callback().replace('cbs', 'pcbs'), cur_key, name, encript_pass)
        getList(u'/', cur_token)
