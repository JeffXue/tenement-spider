# -*- coding:utf-8 -*-
import datetime

from jinja2 import Environment, FileSystemLoader
from numpy import var, average, percentile

env = Environment(loader=FileSystemLoader('./templates'))
report_template = env.get_template('report.html')


def generate_report(data, district, source_web):
    hire_type_count = {'single': 0, 'entire': 0, 'bed': 0,
                       'single_percentile': 0, 'entire_percentile': 0, 'bed_percentile': 0}
    size_price_maps = {
        'r1': {'count': 0, 'prices': [], 'price_size': [], 'avg': 0, 'p5': 0, 'p9': 0, 'variance': 0, 'percentile': 0},
        'r2': {'count': 0, 'prices': [], 'price_size': [], 'avg': 0, 'p5': 0, 'p9': 0, 'variance': 0, 'percentile': 0},
        'r3': {'count': 0, 'prices': [], 'price_size': [], 'avg': 0, 'p5': 0, 'p9': 0, 'variance': 0, 'percentile': 0},
        'r4': {'count': 0, 'prices': [], 'price_size': [], 'avg': 0, 'p5': 0, 'p9': 0, 'variance': 0, 'percentile': 0},
        'r5': {'count': 0, 'prices': [], 'price_size': [], 'avg': 0, 'p5': 0, 'p9': 0, 'variance': 0, 'percentile': 0},
        'r6': {'count': 0, 'prices': [], 'price_size': [], 'avg': 0, 'p5': 0, 'p9': 0, 'variance': 0, 'percentile': 0},
        'r7': {'count': 0, 'prices': [], 'price_size': [], 'avg': 0, 'p5': 0, 'p9': 0, 'variance': 0, 'percentile': 0},
        'r8': {'count': 0, 'prices': [], 'price_size': [], 'avg': 0, 'p5': 0, 'p9': 0, 'variance': 0, 'percentile': 0},
        'r9': {'count': 0, 'prices': [], 'price_size': [], 'avg': 0, 'p5': 0, 'p9': 0, 'variance': 0, 'percentile': 0},
        'r10': {'count': 0, 'prices': [], 'price_size': [], 'avg': 0, 'p5': 0, 'p9': 0, 'variance': 0, 'percentile': 0},
        'total_size_price': []}
    price_count = {'r1': 0, 'r2': 0, 'r3': 0, 'r4': 0, 'r5': 0, 'r6': 0, 'r7': 0, 'r8': 0, 'r9': 0, 'r10': 0,
                   'r1_percentile': 0, 'r2_percentile': 0, 'r3_percentile': 0, 'r4_percentile': 0,
                   'r5_percentile': 0, 'r6_percentile': 0, 'r7_percentile': 0, 'r8_percentile': 0,
                   'r9_percentile': 0, 'r10_percentile': 0}
    hire_type_price_map = {'r1': {'count': 0, 'prices': [], 'avg': 0, 'p5': 0, 'p9': 0, 'variance': 0, 'percentile': 0},
                           'r2': {'count': 0, 'prices': [], 'avg': 0, 'p5': 0, 'p9': 0, 'variance': 0, 'percentile': 0},
                           'r3': {'count': 0, 'prices': [], 'avg': 0, 'p5': 0, 'p9': 0, 'variance': 0, 'percentile': 0},
                           'r4': {'count': 0, 'prices': [], 'avg': 0, 'p5': 0, 'p9': 0, 'variance': 0, 'percentile': 0},
                           'r5': {'count': 0, 'prices': [], 'avg': 0, 'p5': 0, 'p9': 0, 'variance': 0, 'percentile': 0}}
    total = len(data)

    for item in data:

        # 汇总不同租房类型数量
        if item.hire_type == 1:
            hire_type_count['single'] += 1
        if item.hire_type == 2:
            hire_type_count['entire'] += 1
        if item.hire_type == 3:
            hire_type_count['bed'] += 1

        # 汇总不同租房面积数量，及不同面积下租房价格分布数据
        if item.size:
            try:
                size = int(item.size.replace('㎡', ''))
                if size < 100 and int(item.price) < 10000:
                    size_price_maps['total_size_price'].append((size, int(item.price)))
                if size <= 10:
                    size_price_maps['r1']['count'] += 1
                    size_price_maps['r1']['prices'].append(int(item.price))
                    size_price_maps['r1']['price_size'].append((size, int(item.price)))
                if 10 < size <= 20:
                    size_price_maps['r2']['count'] += 1
                    size_price_maps['r2']['prices'].append(int(item.price))
                    size_price_maps['r2']['price_size'].append((size, int(item.price)))
                if 20 < size <= 30:
                    size_price_maps['r3']['count'] += 1
                    size_price_maps['r3']['prices'].append(int(item.price))
                    size_price_maps['r3']['price_size'].append((size, int(item.price)))
                if 30 < size <= 40:
                    size_price_maps['r4']['count'] += 1
                    size_price_maps['r4']['prices'].append(int(item.price))
                    size_price_maps['r4']['price_size'].append((size, int(item.price)))
                if 40 < size <= 50:
                    size_price_maps['r5']['count'] += 1
                    size_price_maps['r5']['prices'].append(int(item.price))
                    size_price_maps['r5']['price_size'].append((size, int(item.price)))
                if 50 < size <= 60:
                    size_price_maps['r6']['count'] += 1
                    size_price_maps['r6']['prices'].append(int(item.price))
                    size_price_maps['r6']['price_size'].append((size, int(item.price)))
                if 60 < size <= 70:
                    size_price_maps['r7']['count'] += 1
                    size_price_maps['r7']['price_size'].append(int(item.price))
                    size_price_maps['r7']['price_size'].append((size, int(item.price)))
                if 70 < size <= 80:
                    size_price_maps['r8']['count'] += 1
                    size_price_maps['r8']['prices'].append(int(item.price))
                    size_price_maps['r8']['price_size'].append((size, int(item.price)))
                if 80 < size <= 90:
                    size_price_maps['r9']['count'] += 1
                    size_price_maps['r9']['prices'].append(int(item.price))
                    size_price_maps['r9']['price_size'].append((size, int(item.price)))
                if 90 < size:
                    size_price_maps['r10']['count'] += 1
                    size_price_maps['r10']['prices'].append(int(item.price))
                    size_price_maps['r10']['price_size'].append((size, int(item.price)))
            except Exception:
                pass

        # 汇总不同租房价格分布
        if item.price:
            price = int(item.price)
            if price <= 1500:
                price_count['r1'] += 1
            if 1500 < price <= 2500:
                price_count['r2'] += 1
            if 2500 < price <= 3500:
                price_count['r3'] += 1
            if 3500 < price <= 4500:
                price_count['r4'] += 1
            if 4500 < price <= 5500:
                price_count['r5'] += 1
            if 5500 < price <= 6500:
                price_count['r6'] += 1
            if 6500 < price <= 7500:
                price_count['r7'] += 1
            if 7500 < price <= 8500:
                price_count['r8'] += 1
            if 8500 < price <= 9500:
                price_count['r9'] += 1
            if 9500 < price:
                price_count['r10'] += 1

        # 汇总不同整租户型数量，及不同户型下租房价格分布数据
        if item.hire_type == 2:
            if item.abstract_size.find('1室') != -1:
                hire_type_price_map['r1']['count'] += 1
                hire_type_price_map['r1']['prices'].append(int(item.price))
            elif item.abstract_size.find('2室') != -1:
                hire_type_price_map['r2']['count'] += 1
                hire_type_price_map['r2']['prices'].append(int(item.price))
            elif item.abstract_size.find('3室') != -1:
                hire_type_price_map['r3']['count'] += 1
                hire_type_price_map['r3']['prices'].append(int(item.price))
            elif item.abstract_size.find('4室') != -1:
                hire_type_price_map['r4']['count'] += 1
                hire_type_price_map['r4']['prices'].append(int(item.price))
            else:
                hire_type_price_map['r5']['count'] += 1
                hire_type_price_map['r5']['prices'].append(int(item.price))

    hire_type_count_total = hire_type_count['single'] + hire_type_count['entire'] + hire_type_count['bed']
    if hire_type_count_total:
        hire_type_count['single_percentile'] = '%0.3f' % float(hire_type_count['single'] * 100 / hire_type_count_total)
        hire_type_count['entire_percentile'] = '%0.3f' % float(hire_type_count['entire'] * 100 / hire_type_count_total)
        hire_type_count['bed_percentile'] = '%0.3f' % float(hire_type_count['bed'] * 100 / hire_type_count_total)

    price_count_total = price_count['r1'] + price_count['r2'] + price_count['r3'] + price_count['r4'] + price_count[
        'r5'] + price_count['r6'] + price_count['r7'] + price_count['r8'] + price_count['r9'] + price_count['r10']
    if price_count_total:
        price_count['r1_percentile'] = int(price_count['r1'] * 100 / price_count_total)
        price_count['r2_percentile'] = int(price_count['r2'] * 100 / price_count_total)
        price_count['r3_percentile'] = int(price_count['r3'] * 100 / price_count_total)
        price_count['r4_percentile'] = int(price_count['r4'] * 100 / price_count_total)
        price_count['r5_percentile'] = int(price_count['r5'] * 100 / price_count_total)
        price_count['r6_percentile'] = int(price_count['r6'] * 100 / price_count_total)
        price_count['r7_percentile'] = int(price_count['r7'] * 100 / price_count_total)
        price_count['r8_percentile'] = int(price_count['r8'] * 100 / price_count_total)
        price_count['r9_percentile'] = int(price_count['r9'] * 100 / price_count_total)
        price_count['r10_percentile'] = int(price_count['r10'] * 100 / price_count_total)

    for key, value in size_price_maps.iteritems():
        if key != 'total_size_price' and value['prices']:
            size_price_maps[key]['avg'] = int(average(value['prices']))
            size_price_maps[key]['p5'] = int(percentile(value['prices'], 50))
            size_price_maps[key]['p9'] = int(percentile(value['prices'], 90))
            size_price_maps[key]['variance'] = int(var(value['prices']))

    for key, value in hire_type_price_map.iteritems():
        if value['prices']:
            hire_type_price_map[key]['avg'] = int(average(value['prices']))
            hire_type_price_map[key]['p5'] = int(percentile(value['prices'], 50))
            hire_type_price_map[key]['p9'] = int(percentile(value['prices'], 90))
            hire_type_price_map[key]['variance'] = int(var(value['prices']))

    date = datetime.datetime.now().date()
    html = report_template.render(total=total, district=district, date=date,
                                  hire_type_count=hire_type_count, price_count=price_count,
                                  size_price_maps=size_price_maps, hire_type_price_map=hire_type_price_map)

    html_file = 'report/%s_%s_%s.html' % (source_web, district, datetime.datetime.now().date())
    with open(html_file, 'w') as f:
        f.write(html.encode('utf-8'))
