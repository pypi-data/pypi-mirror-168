#!/usr/bin/env python
# encoding: utf-8
"""
@author: brill
@file: qbasenative.py
@time: 2019/7/22 10:35 AM
@desc:
"""
# !/usr/bin/env python3
# Created by xiazeng on 2019-05-22
from minium.native.wx_native.basenative import BaseNative


class QBaseNative(BaseNative):
    def __init__(self, json_conf):
        super(BaseNative, self).__init__()
        self.json_conf = json_conf

    def open_remote_debug(self, scheme_url):
        raise NotImplementedError()

    def release(self):
        raise NotImplementedError()

    def start_qq(self):
        """
        启动QQ
        :return:
        """
        raise NotImplementedError()

    def stop_qq(self):
        """
        启动QQ
        :return:
        """
        raise NotImplementedError()


class NativeError(RuntimeError):
    pass
