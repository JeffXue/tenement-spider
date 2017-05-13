# -*- coding:utf-8 -*-


class Model:

    def __init__(self):
        # 源站点
        self.source_web = None

        # 租房类型
        # 单间: 1
        # 整租: 2
        # 床位: 3
        self.hire_type = None

        # 原文章标题
        self.title = None

        # 原文章URL
        self.url = None

        # 抽象大小
        self.abstract_size = None

        # 面积
        self.size = None

        # 位置
        self.district = None

        # 小区,如花园 村等
        self.position = None

        # 房源
        # 个人: 0
        # 中介: 1
        self.source_type = None

        # 发布时间
        self.release_time = None

        # 价格
        self.price = None
