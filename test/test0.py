'''
@author: Zxh
'''
from arm_project.scheduler import Scheduler

b = 4;
c = 4;


def a():
    global b, c
    try:
        print b / c;
    except:
        print 'error'
    finally:
        c = c - 1


if __name__ == '__main__':
    a()
    s = Scheduler(1, a)
    s.start();
