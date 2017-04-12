# -*- coding:utf-8 -*-
import requests

from sgmllib import SGMLParser

from model import Model


class SelfParser(SGMLParser):
    def __init__(self):
        self.start_flag = False
        self.des_div_flag = False
        self.title_flag = False
        self.room_flag = False
        self.add_flag = False
        self.geren_flag = False
        self.sendTime_flag = False
        self.money_flag = False
        self.data = []
        self.model = None
        self.location = ''
        SGMLParser.__init__(self)

    def start_li(self, attrs):
        count = 0
        for key, value in attrs:
            if key == 'logr':
                count += 1
            if key == 'sortid':
                count += 1
        if count == 2:
            self.model = Model()
            self.model.source_web = '58'
            self.start_flag = True

    def end_li(self):
        self.start_flag = False
        self.data.append(self.model)
        self.model = None

    def start_div(self, attrs):
        for key, value in attrs:
            if key == 'class' and value == 'des':
                if self.start_flag:
                    self.des_div_flag = True
            if key == 'class' and value == 'sendTime':
                if self.start_flag:
                    self.sendTime_flag = True
            if key == 'class' and value == 'money':
                if self.start_flag:
                    self.money_flag = True

    def end_div(self):
        self.des_div_flag = False
        self.sendTime_flag = False
        self.money_flag = False

    def start_a(self, attrs):
        for key, value in attrs:
            if key == 'tongji_label':
                if self.des_div_flag:
                    self.title_flag = True

    def end_a(self):
        self.title_flag = False

    def start_p(self, attrs):
        for key, value in attrs:
            if key == 'class' and value == 'room':
                if self.des_div_flag:
                    self.room_flag = True
            if key == 'class' and value == 'add':
                if self.des_div_flag:
                    self.add_flag = True
            if key == 'class' and value == 'geren':
                if self.des_div_flag:
                    self.geren_flag = True

    def end_p(self):
        self.room_flag = False
        self.add_flag = False
        self.geren_flag = False

    def handle_data(self, data):
        if data.strip() != "":
            if self.title_flag:
                if data.find('单间') != -1:
                    self.model.hire_type = 1
                if data.find('整租') != -1:
                    self.model.hire_type = 2
                if data.find('床位') != -1:
                    self.model.hire_type = 3
                self.model.title = data.strip().split('|')[-1].strip()
            if self.room_flag:
                self.model.size = data.strip().split()[-1].replace('&nbsp;', '').split('m')[0]
                self.model.abstract_size = data.strip().split()[0]
            if self.add_flag:
                self.location += data
            if self.geren_flag:
                if data.find('个人房源') != -1:
                    self.model.source_type = 0
                if data.find('经纪人') != -1:
                    self.model.source_type = 1
            if self.sendTime_flag:
                pass
            if self.money_flag:
                if data.strip().find('元') == -1:
                    self.model.price = data.strip()

    def work(self):
        print self.data[0].source_web
        print self.data[0].hire_type
        print self.data[0].title
        print self.data[0].abstract_size
        print self.data[0].size
        print self.data[0].district
        print self.data[0].position
        print self.data[0].source_type
        print self.data[0].price
        return self.data


def spider_one_page(url):
    r = requests.get(url)
    with open('../temp/58.html', 'w') as f:
        f.write(r.content)

    parser = SelfParser()
    with open('../temp/58.html', 'r') as f:
        for line in f.readlines():
            parser.feed(line)
    data = parser.work()

    try:
        next_url = r.text.split('<a  class="next" href="')[-1].split('"><span>')[0]
    except Exception:
        next_url = None
    return next_url, data


def spider_58():
    url = 'http://sz.58.com/chuzu/0/'
    nexl_url, data = spider_one_page(url)
    print nexl_url


if __name__ == '__main__':
    spider_58()
