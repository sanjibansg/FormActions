import os
import sys
import logging
import colorlog
import datetime

def remove_old(path):
    for root,directories,files in os.walk(path,topdown=False):
        for name in files:
            t = os.stat(os.path.join(root, name))[8]
            filetime = datetime.datetime.fromtimestamp(t) - datetime.datetime.today()
            if filetime.days <= -7:
                os.remove(os.path.join(root, name))

def logger(name):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    if not os.path.exists('logs'):
        os.makedirs('logs')
    remove_old("logs/")
    fileLog   = logging.FileHandler("logs/LOG_"+str(datetime.date.today())+".log",'a')
    screenLog = logging.StreamHandler(sys.stdout)
    fileLog.setFormatter(colorlog.ColoredFormatter('[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s', datefmt='%a, %d %b %Y %H:%M:%S'))
    screenLog.setFormatter(colorlog.ColoredFormatter('%(log_color)s [%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s', datefmt='%a, %d %b %Y %H:%M:%S'))
    log.addHandler(screenLog)
    log.addHandler(fileLog)
    return log
