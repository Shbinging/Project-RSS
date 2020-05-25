import time

def time_stamp():
    now = int(time.time())
    timeArray = time.localtime(now)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S",timeArray)
    return otherStyleTime

def log():
    __time = ''
    __log = ''
    __fp = ''
    def __init__(self):
        __time = time_stamp()
        __fp = open("./log/log.txt","a+")
    def write_log(self):
        self.__fp.writelines

    


        