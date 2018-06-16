import itchat as ic

ic.auto_login()
ic.send('Hello from PC-Hakim', toUserName='filehelper')

# 获取好友列表
friends = ic.get_friends(update=True)[0:]

# 初始化计数器，有男有女，当然，有些人是不填的
male = female = other = 0

# 遍历这个列表，列表里第一位是自己，所以从"自己"之后开始计算
# 1表示男性，2女性
for i in friends[1:]:
    sex = i["Sex"]
    if sex == 1:
        male += 1
    elif sex == 2:
        female += 1
    else:
        other += 1

# 总数算上，好计算比例啊～
total = len(friends[1:])

# 好了，打印结果
print(u'一共有好友：%d'%total)
print(u"男性好友一共：%d， 占比：%.2f%%" % (male,(float(male) / total * 100)))
print(u"女性好友一共：%d， 占比：%.2f%%" % (female,(float(female) / total * 100)))
print(u"其他：%.2f%%" % (float(other) / total * 100))