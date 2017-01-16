'''

@author: Zxh
'''
from time import sleep

from arm_project.currenttime import get_time

a = "2016-06-15 8:30"
b = "1015"
print a > b
a = [1,
     3,
     5]
print a
a = 0.0
print a == 0
a = 7
b = "6"
print a > b
a = get_time()
sleep(10)
b = get_time()
print b - a