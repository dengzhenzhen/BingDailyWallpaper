import logging
import json
import os

with open('D:\\Repositories\\BingDailyWallpaper\\config.json', 'r') as fp:
    config = json.load(fp)

log_path = config.get('logPath')
dir_name = os.path.dirname(log_path)
if not os.path.exists(dir_name):
    os.makedirs(dir_name)

logging.basicConfig(filename=log_path,
                    format="%(asctime)s|%(threadName)s|%(levelname)s|%(msg)s",
                    level=logging.INFO)

def log(func):
    def inner(*args, **kwargs):
        logging.info("{0}, {1}, {2}".format(func.__name__, [str(i) for i in args], kwargs))
        return func(*args, **kwargs)
    return inner

@log
def aaa(a,b,c=1):
    return a+b+c

if __name__ == "__main__":
    aaa(1, 3, c=5)
    