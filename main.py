import requests
import bs4
import threading
import datetime
import os
import json
import time
from log_manager import log, CONFIG_PATH

class Bing:
    def __init__(self):
        self.base_url = "http://cn.bing.com"
        self.main_page = ""
        self.img_url = ""
        self.image_name = ""
        self.save_path = ""
        self.img_dir = ""
        self.stop = False
        self.get_config(CONFIG_PATH)
        self.update()

    def update(self):
        _, self.main_page = self.get_main_page()
        self.img_url = self.get_img_url()
        self.update_save_path()


    def get_main_page(self):
        ret, content = self.http_request(requests.get, self.base_url)
        if ret:
            return ret, content
        else:
            return False, content 

    def get_img_url(self):
        soup = bs4.BeautifulSoup(self.main_page, features="html.parser")
        src = soup.find(attrs={'id':'bgImgProgLoad'}).get("data-ultra-definition-src")
        return self.base_url + src

    @log
    def save_img(self):
        ret, img = self.http_request(requests.get, self.img_url)
        if ret:
            with open(self.save_path, 'wb') as fp:
                fp.write(img)
            return True
        else:
            return False
    
    @log
    def http_request(self, request_method, url, payloads={}, retries=3):
        for i in range(retries):
            res = request_method(url, payloads)
            if res.status_code == 200:
                return True, res.content
            if i == 2:
                return False, res.content
            time.sleep(1)

    def update_save_path(self):
        date = datetime.date.today()
        if not os.path.exists(self.img_dir):
            os.makedirs(self.img_dir)
        save_path = os.path.join(self.img_dir, self.image_name.format(date=date))
        self.save_path = save_path
        return self.save_path

    def get_config(self, config_path):
        with open(config_path, 'r') as fp:
            config = json.load(fp)
        self.img_dir = config.get('saveDir')
        self.image_name = config.get('imageName')
        self.waiting_sec = config.get('waitingTime')
    
    def set_waiting_time(self, waiting_sec):
        self.waiting_sec = waiting_sec

    @log
    def run(self):
        self.isalive = True
        daemon_thread = threading.Thread(target=self.daemon)
        daemon_thread.start()
        try:
            while True:
                if os.path.exists(self.update_save_path()):
                    time.sleep(self.waiting_sec)
                elif self.stop:
                    break
                else:
                    self.update()
                    self.save_img()
        except Exception as err:
            print(err)
        finally:
            self.isalive = False

    @log
    def daemon(self):
        while self.isalive:
            time.sleep(1)
        try:pass
        finally:
            if not self.stop:
                self.run()

    def stop_running(self):
        self.stop = True

    def __str__(self):
        return "Bing"

if __name__ == "__main__":
    bing = Bing()
    bing.run()
