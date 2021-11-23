import sys
import logging
import colorlog
import datetime

def logging():
    log = logging.getLogger('')
    log.setLevel(logging.DEBUG)
    fileLog   = logging.FileHandler("LOG_"+datetime.datetime.now())
    screenLog = logging.StreamHandler(sys.stdout)
    screenLog.setFormat(colorlog.ColoredFormatter('%(log_color)s [%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s', datefmt='%a, %d %b %Y %H:%M:%S'))
    fileLog.setFormat( logging.Formatter('[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s', datefmt='%a, %d %b %Y %H:%M:%S'))
    log.addHandler(screenLog)
    log.addHandler(fileLog)
    return log
