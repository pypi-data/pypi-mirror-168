#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------------------
# ProjectName: logcat_monitor
# Author: Gent Liu
# CreateTime: 2022/9/21 12:52
# File Name: statistics
# Description:
# --------------------------------------------------------------
class Statistics:
    """
    统计类
    """

    def increase(self, key_dict, key):
        """
        增加异常次数
        :param key_dict:
        :param key:
        :return:
        """
        if key in key_dict:
            attr = key_dict[key]
            count = getattr(self, attr, 0)
            target = count + 1
            setattr(self, attr, target)
            print("捕获到异常[%s]，当前此类异常数为:%d" % (key, target))
