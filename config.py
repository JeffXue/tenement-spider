# -*- coding:utf-8 -*-
import ConfigParser


class Config:
    """get config from the ini file"""

    def __init__(self, config_file):
        all_config = ConfigParser.ConfigParser()
        with open(config_file, 'r') as cfg_file:
            all_config.readfp(cfg_file)

        self.url_58 = all_config.get('url', '58')

config = Config('conf/config.ini')
