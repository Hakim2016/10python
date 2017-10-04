# 10python

Zhihu login!

20171004
    dict163 login
    The request headers vary from different requests(like login requests and wordbook requests)
    Need to construct different headers.

        login_code = session.get(wrdbk_url, headers=headers, allow_redirects=False).status_code
        不允许重定向 遇到重定向的网址 会报错
