# -*- coding:utf-8 -*-
import time
from sgmllib import SGMLParser

import requests

from model import Model


class SelfParser(SGMLParser):
    def __init__(self):
        self.start_flag = False
        self.des_div_flag = False
        self.title_flag = False
        self.room_flag = False
        self.add_flag = False
        self.district_flag = False
        self.position_flag = False
        self.geren_flag = False
        self.sendTime_flag = False
        self.money_flag = False
        self.pager_flag = False
        self.data = []
        self.model = None
        self.next_url = None
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
        if self.model and self.model.price and self.model.price.isdigit():
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
            if key == 'class' and value == 'pager':
                self.pager_flag = True

    def end_div(self):
        self.des_div_flag = False
        self.sendTime_flag = False
        self.money_flag = False
        self.pager_flag = False

    def start_a(self, attrs):
        keys = []
        next_page_flag = False
        for key, value in attrs:
            if key == 'tongji_label':
                if self.des_div_flag:
                    self.title_flag = True
                    self.model.url = attrs[0][1]
            if key == 'class' and value == 'next' and self.pager_flag:
                next_page_flag = True
            if next_page_flag and key == 'href':
                self.next_url = value
            keys.append(key)
        if self.add_flag and 'target' in keys:
            self.district_flag = True
        if self.add_flag and 'target' not in keys:
            self.position_flag = True

    def end_a(self):
        self.title_flag = False
        self.district_flag = False
        self.position_flag = False

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
                self.model.title = data.strip().split('|')[-1].strip().replace(',', '、').replace('，', '、')
            if self.room_flag:
                data = data.split('&nbsp;')[0]
                if data.find('㎡') != -1:
                    self.model.size = data.split('&nbsp;')[-1].strip()
                else:
                    self.model.abstract_size = data.split('&nbsp;')[0].strip().replace(',', '、').replace('，', '、')
            if self.district_flag:
                self.model.district = data.strip().replace(',', '、').replace('，', '、')
            if self.position_flag:
                self.model.position = data.strip().replace(',', '、').replace('，', '、')
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
        # print self.data[0].source_web, self.data[0].hire_type, self.data[0].title, self.data[0].abstract_size, self.data[0].size, self.data[0].district, self.data[0].position, self.data[0].source_type, self.data[0].price
        return self.next_url, self.data


def spider_one_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    r = requests.get(url, headers=headers)
    with open('58_temp.html', 'w') as f:
        f.write(r.content)

    parser = SelfParser()
    with open('58_temp.html', 'r') as f:
        for line in f.readlines():
            parser.feed(line)

    return parser.work()


def spider_58(url, total_data):
    print url
    next_url, data = spider_one_page(url)
    total_data.extend(data)
    if next_url:
        time.sleep(0.1)
        spider_58(next_url, total_data)


if __name__ == '__main__':
    # data_58 = []
    # spider_58('http://sz.58.com/chuzu/0/', data_58)
    next_url, data = spider_one_page('http://sz.58.com/chuzu/0/')
    for item in data:
        print str(item.source_web) + ' ' + str(item.hire_type) + ' ' + str(item.title) + ' ' + str(
            item.abstract_size) + ' ' + str(item.size) + ' ' + str(item.district) + ' ' + str(
            item.position) + ' ' + str(item.source_type) + ' ' + str(item.price) + ' ' + str(item.url)
