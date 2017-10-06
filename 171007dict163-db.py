import pymysql as mysql

conn = mysql.connect(host='localhost', user='root', passwd='root', db='testdb', port=3306)


# user cursor() to get cursor operation
cursor = conn.cursor()

def add():
    pass

def dlt():
    pass

def updt():
    pass

def slct():
    pass

# SQL insert into table employee
sql = """insert into employee(first_name, last_name, age, sex, income)
         values('Hakim', 'He', 20, 'M', 7000)"""

try:
    # execute this sql
    cursor.execute(sql)
    # commit to mysql datebase to execute
    conn.commit()
except:
    print('error happens')
    # if err happens rollback
    conn.rollback()

# close the connecttion
conn.close()