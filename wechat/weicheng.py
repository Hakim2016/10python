import itchat as ic
ic.auto_login()

# 获取特定UserName的公众号，返回值为一个字典
qishu = ic.search_mps(userName='@qishuGRE')

print(qishu)
# 获取名字中含有特定字符的公众号，返回值为一个字典的列表
# itchat.search_mps(name='gzh')
# 以下方法相当于仅特定了UserName
# itchat.search_mps(userName='@abcdefg1234567', name='gzh')