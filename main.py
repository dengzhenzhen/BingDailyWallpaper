import requests
import bs4
import threading
import datetime
import os
import json
import time
import smtplib

from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart

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
        self.enable_mail = False
        self.mail = Mail()
        self.get_config(CONFIG_PATH)
        self.mail.load_config(CONFIG_PATH)
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
                if self.enable_mail:
                    self.mail.send_image(img)
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
        self.enable_mail = config.get('enableMail')

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

class Mail:
    def __init__(self):
        self.user = None
        self.password = None
        self.from_addr = None
        self.to_addr_list = None

    def load_config(self, config_path):
        with open(config_path, 'r') as fp:
            config = json.load(fp)
        self.user = config.get('userName')
        self.password = config.get('passwd')
        self.from_addr = config.get('From')
        self.to_addr_list = config.get('To')

    def send_image_to(self, img_bytes, to_addr):
        # demo
        mail = MIMEMultipart()
        mail['From'] = Header(self.from_addr)
        mail['To'] = Header(to_addr)
        mail['Subject'] = Header('今日壁纸')
        mail.attach(MIMEText('今日壁纸'))
        attachment = MIMEText(img_bytes, 'base64', 'utf-8')
        attachment['Content-Type'] = 'application/octet-stream'
        attachment['Content-Disposition'] = 'attachment;filename="hello.jpg"'
        mail.attach(attachment)
        server = smtplib.SMTP('smtp.qq.com')
        account = self.user
        password = self.password
        server.login(account, password)
        server.sendmail(account, account, mail.as_string())
        server.quit()

    @log
    def send_image(self, img_bytes):
        mail_list = []
        for to_addr in self.to_addr_list:
            date = datetime.date.today()
            mail = MIMEMultipart()
            mail['From'] = Header(self.from_addr)
            mail['To'] = Header(to_addr)
            mail['Subject'] = Header('今日壁纸{date}'.format(date=date ))
            mail.attach(MIMEText('{0}'.format(date)))

            attachment = MIMEText(img_bytes, 'base64', 'utf-8')
            attachment['Content-Type'] = 'application/octet-stream'
            attachment['Content-Disposition'] = 'attachment;filename="{0}.jpg"'.format(date)
            mail.attach(attachment)
            mail_list.append({'mail':mail, 'to_addr':to_addr})

        server = smtplib.SMTP('smtp.qq.com')
        account = self.user
        password = self.password
        server.login(account, password)
        for mail in mail_list:
            server.sendmail(account, mail['to_addr'], mail['mail'].as_string())
        server.quit()


def main():
    # mail = Mail()
    # mail.load_config(CONFIG_PATH)
    # mail.send_image(b"")
    bing = Bing()
    bing.run()


if __name__ == "__main__":
    main()
