# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
# Created Time: 2015年12月08日 星期二 13时41分25秒
#
'''
    project的持久化对象
'''
class Project(object):
    '''
        Project的持久化类
        读入参数生成对应project对象
        从而可以生成一个html格式的字符串
    '''
    def __init__(self, line):
        args = line.split(',')
        try:
            assert len(args) == 4
        except:
            print args
        args = [arg.strip() for arg in args]
        self.name = args[0]
        self.start_time = args[1]
        self.end_time = args[2]
        self.item = args[3]

    def __str__(self):
        pre_strs = [
            self.name,
            self.start_time,
            self.end_time,
            '<br />'.join(self.item.split('|')),
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
