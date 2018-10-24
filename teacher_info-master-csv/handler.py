# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
# Created Time: 2015年12月08日 星期二 11时41分40秒
#
'''
    Read the csv and generate a html-format string
'''


def handle(model='paper'):
    #Some preparation
    final_str = ''

    # Import model
    cls = __import__(model)
    cls = getattr(cls, model.capitalize())
    
    # Read csv
    with open(model+'.csv') as f:
        for line in f:
            # Instance
            instance = cls(line)
            # Generate str
            final_str = '\n'.join((final_str, str(instance)))
    
    # Write str
    with open(model+'.txt', 'w') as f:
        f.write(final_str)

handle(model='project')
