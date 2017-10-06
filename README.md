# 10python

Zhihu login!

20171004
    dict163 login
    The request headers vary from different requests(like login requests and wordbook requests)
    Need to construct different headers.

        login_code = session.get(wrdbk_url, headers=headers, allow_redirects=False).status_code
        不允许重定向 遇到重定向的网址 会报错
20171005
        配置plsql 保存常用的单词
        设计表格(存放单词的解释太占用资源了！）
        CREATE TABLE IF NOT EXISTS `runoob_tbl`(
           `runoob_id` INT UNSIGNED AUTO_INCREMENT,
           `runoob_title` VARCHAR(100) NOT NULL,
           `runoob_author` VARCHAR(40) NOT NULL,
           `submission_date` DATE,
           PRIMARY KEY ( `runoob_id` )
        )ENGINE=InnoDB DEFAULT CHARSET=utf8;

        create table if not exists words(
            wrd_id int auto_increment primary key,
            word varchar(50) unique key,
            meaning varchar(200),
            add_time date,
            cate_id int)ENGINE=InnoDB DEFAULT CHARSET=utf8;



        # 创建中文报错 需要制定存放的字符类型
        drop table categories;
        create table if not exists categories(
            cate_id int auto_increment primary key,
            cate_name varchar(40),
            create_time date)ENGINE=InnoDB DEFAULT CHARSET=utf8;
        insert into categories(cate_name) values('晶晶');




