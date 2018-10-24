# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
# Created Time: 2015年12月08日 星期二 11时41分40秒
#
'''
    paper的持久化对象
'''
class Paper(object):
    '''
        Paper的持久化类
        读入参数生成对应paper对象
        从而可以生成一个html格式的字符串
    '''
    def __init__(self, line):
        temps = line.split('"')
        args = []
        args.append(temps[1])
        args.extend(temps[2].split(',')[1:])
        assert len(args) == 8
        args = [arg.strip() for arg in args]
        self.author = args[0]
        self.title = args[1]
        self.volume = args[2]
        self.number = args[3]
        self.start_page = args[4]
        self.end_page  =args[5]
        self.publish_year = args[6]
        self.publisher_name = args[7]

    def __str__(self):
        pre_strs = [
            self.author,
            self.title,
            ''.join(
                (
                    'Vol.'+self.volume if self.volume else '',
                    ' No.'+self.number if self.number else '',
                    ' pp.'+self.start_page+'-'+self.end_page,
                )
            ),
            self.publish_year[-4:],
            self.publisher_name,
        ]
        pre_strs =\
            [
                ''.join(
                    (
                        '<td style="border-top-style:solid;',
                        'border-top-width:1px;border-top-c',
                        'olor:#E6E6E6;padding:8px">',
                        pre_str,
                        '</td>',
                    )
                ) for pre_str in pre_strs
            ]
        return '<tr>' + ''.join(pre_strs) + '</tr>'
