import pymysql as mysql
import time
import traceback

# conn = mysql.connect(host='localhost', user='root', passwd='root', db='youdaodb', port=3306)
# youdao_add(word[i],wrd_time[i],tags[wrd_tag[i]])
def youdao_add(word, datestr, tag):
    date = time.strptime(datestr, '%Y-%m-%d')
    tag = int(tag)
    conn = mysql.connect(host='localhost', user='root', passwd='root', db='youdaodb', port=3306)
    # user cursor() to get cursor operation
    cursor = conn.cursor()
    sql = """
        insert into words(word, add_time,cate_id) values(%s,%s,%s)
    """
    params = (word,date,tag)
    try:
        # execute this sql
        cursor.execute(sql, params)
        conn.commit()
    except:
        print('error happens')
        traceback.print_exc()
        # if err happens rollback
        conn.rollback()
    finally:
        # close the connecttion
        conn.close()
    pass

def youdao_dlt():
    pass

def youdao_updt():
    pass

def youdao_slct():
    pass

def youdao_lst():
    result = {}
    conn = mysql.connect(host='localhost', user='root', passwd='root', db='youdaodb', port=3306)
    # user cursor() to get cursor operation
    cursor = conn.cursor()
    sql = """
        select cate_id, cate_name from categories
    """
    try:
        # execute this sql
        cursor.execute(sql)
        cnt = cursor.fetchall()
    except:
        print('error happens')
        # if err happens rollback
        conn.rollback()
    finally:
        # close the connecttion
        conn.close()
    return cnt

def yd_cate_cnt():
    conn = mysql.connect(host='localhost', user='root', passwd='root', db='youdaodb', port=3306)
    # user cursor() to get cursor operation
    cursor = conn.cursor()
    sql = """
        select count(1) from categories
    """
    try:
        # execute this sql
        cursor.execute(sql)
        cnt = cursor.fetchone()[0]

    except:
        print('error happens')
        # if err happens rollback
        conn.rollback()
    finally:
        # close the connecttion
        conn.close()
    return cnt

# # SQL insert into table employee
# sql = """insert into employee(first_name, last_name, age, sex, income)
#          values('Hakim', 'He', 20, 'M', 7000)"""

if __name__ == '__main__':
    youdao_add('Dairy', '2017-08-03', 3)
    pass

# try:
#     # execute this sql
#     cursor.execute(sql)
#     # commit to mysql datebase to execute
#     conn.commit()
# except:
#     print('error happens')
#     # if err happens rollback
#     conn.rollback()
#
# # close the connecttion
# conn.close()