# coding=utf-8

import time


def get_current_time():
    local_time = time.localtime(time.time())
    return time.strftime("%Y-%m-%d %X", local_time)


# return "2016-16-16 12:21"
def get_current_month():
    local_time = time.localtime(time.time())
    return "%s" % (local_time[1])


def get_current_hour():
    local_time = time.localtime(time.time())
    return "%s" % (local_time[3])


def get_time():
    return time.time()


if __name__ == '__main__':
    print get_current_time()
    print time.time()
    print time.localtime(time.time())
    print get_current_month()
    print get_current_hour()
    print get_time()
