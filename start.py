# -*- coding:utf-8 -*-
import os
import time
import datetime

from report import generate_report
from spiders.spider58 import spider_58


def csv_data(source_web, district, data):
    with open('report/%s_%s_%s.csv' % (source_web, district, datetime.datetime.now().date()), 'a+') as f:
        f.write('源站点,租房类型,标题,室厅卫,面积,小区,地区,房源,价格,原文链接\r\n')
        for item in data:
            if item.hire_type == 1:
                hire_type = '单间'
            if item.hire_type == 2:
                hire_type = '整租'
            if item.hire_type == 3:
                hire_type = '床位'

            if item.source_type == 0:
                source_type = '个人'
            if item.source_type == 1:
                source_type = '中介'

            f.write(str(item.source_web) + ',' + str(hire_type) + ',' + str(item.title) + ',' +
                    str(item.abstract_size) + ',' + str(item.size) + ',' + str(item.district) + ',' +
                    str(item.position) + ',' + str(source_type) + ',' + str(item.price) + ',' + str(item.url) + '\r\n')


def had_analysed(source_web, district):
    files = [item for item in os.listdir('report/')]
    target_file = '%s_%s_%s.html' % (source_web, district, datetime.datetime.now().date())
    for report_file in files:
        if report_file.find('html') == -1:
            continue
        if report_file == target_file.encode('utf-8'):
            return True
    return False


def main():
    target_58_configs = [('http://sz.58.com/chuzu/0/', u'不限'),
                         ('http://sz.58.com/luohu/chuzu/0/', u'罗湖'),
                         ('http://sz.58.com/futian/chuzu/0/', u'福田'),
                         ('http://sz.58.com/nanshan/chuzu/0/', u'南山'),
                         ('http://sz.58.com/yantian/chuzu/0/', u'盐田'),
                         ('http://sz.58.com/baoan/chuzu/0/', u'宝安'),
                         ('http://sz.58.com/longgang/chuzu/0/', u'龙岗'),
                         ('http://sz.58.com/buji/chuzu/0/', u'布吉'),
                         ('http://sz.58.com/pingshanxinqu/chuzu/0/', u'坪山新区'),
                         ('http://sz.58.com/guangmingxinqu/chuzu/0/', u'光明新区'),
                         ('http://sz.58.com/szlhxq/chuzu/0/', u'龙华新区'),
                         ('http://sz.58.com/dapengxq/chuzu/0/', u'大鹏新区')]

    for config in target_58_configs:
        url = config[0]
        district = config[1]

        if had_analysed('58', district):
            continue

        data = []
        spider_58(url, data)
        csv_data('58', district, data)
        generate_report(data, district, '58')
        time.sleep(5)


if __name__ == '__main__':
    main()
