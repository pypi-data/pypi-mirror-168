#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
Author:         lockerzhang
Filename:       minium_object.py
Create time:    2019/4/30 21:21
Description:

"""

from .minium_log import MonitorMetaClass
from .callback import Callback
from .connection import Command, Connection
from ...utils.injectjs import getInjectJsCode
import subprocess
import time
import logging
import types

logger = logging.getLogger("minium")


class MiniumObject(object, metaclass=MonitorMetaClass):
    _cant_use_interface = {}

    def __init__(self):
        self.logger = logger
        self.observers = {}
        self.connection: Connection = None

    def _do_shell(self, command, print_msg=True, input=b""):
        """
        执行 shell 语句
        :param command:
        :param print_msg:
        :return:
        """
        self.logger.info("de shell: %s" % command)
        p = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )
        out, err = p.communicate(input)
        try:
            out = out.decode("utf8")
        except UnicodeDecodeError:
            out = out.decode("gbk")
        try:
            err = err.decode("utf8")
        except UnicodeDecodeError:
            err = err.decode("gbk")
        if print_msg:
            self.logger.info("err:\n%s" % err)
            self.logger.info("out:\n%s" % out)
        return out, err

    @classmethod
    def _can_i_use(cls, name):
        return not cls._cant_use_interface.get(name, False)

    @classmethod
    def _unset_interface(cls, name):
        cls._cant_use_interface[name] = True

    def call_wx_method(self, method, args=None, plugin_appid="auto"):
        """
        调用 wx 的方法
        :param method:
        :param args:
        :param plugin_appid: 调用插件[${appid}]中的方法
        :return:
        """
        if plugin_appid == "auto":
            plugin_appid = None
        return self._call_wx_method(method=method, args=args, plugin_appid=plugin_appid)

    def mock_wx_method(
        self,
        method,
        functionDeclaration: str = None,
        result=None,
        args=None,
        success=True,
        plugin_appid="auto",
    ):
        """
        mock wx method and return result
        :param self:
        :param method:
        :param functionDeclaration:
        :param result:
        :param args:
        :param success:
        :return:
        """
        if plugin_appid == "auto":
            plugin_appid = None
        self._mock_wx_method(
            method=method,
            functionDeclaration=functionDeclaration,
            result=result,
            args=args,
            success=success,
            plugin_appid=plugin_appid,
        )

    def restore_wx_method(self, method, plugin_appid="auto"):
        """
        恢复被 mock 的方法
        :param method: mock的方法
        :param plugin_appid: 插件appid
        :return:
        """
        params = {"method": method}
        if plugin_appid == "auto":
            plugin_appid = None
        if plugin_appid:
            params["pluginId"] = plugin_appid
        self.connection.send("App.mockWxMethod", params)

    def hook_wx_method(self, method: str, before: Callback or types.FunctionType=None, after: Callback or types.FunctionType=None, callback: Callback or types.FunctionType=None):
        """
        hook wx 方法
        :param method: 需要 hook 的方法
        :param before: 在需要 hook 的方法之前调用
        :param after: 在需要 hook 的方法之后调用
        :param callback: 在需要 hook 的方法回调之后调用
        :return:
        """

        if isinstance(before, Callback):
            before = before.callback
        if isinstance(after, Callback):
            after = after.callback
        if isinstance(callback, Callback):
            callback = callback.callback

        def super_before(msg):
            self.logger.debug(f"{method} before hook result: {msg['args']}")
            if before:
                before(msg["args"])

        if before and not callable(before):
            self.logger.error(f"wx.{method} hook before method is non-callable")
            return
        if before:
            self._expose_function(method + "_" + super_before.__name__, super_before)

        def super_after(msg):
            self.logger.debug(f"wx.{method} after hook result: {msg['args']}")
            if after:
                after(msg["args"])

        if after and not callable(after):
            self.logger.error(f"{method} hook after method is non-callable")
            return
        if after:
            self._expose_function(method + "_" + super_after.__name__, super_after)

        def super_callback(msg):
            self.logger.debug(f"wx.{method} callback hook result: {msg['args']}")
            if callback:
                callback(msg["args"])

        if callback and not callable(callback):
            self.logger.error(f"{method} hook callback method is non-callable")
            return
        if callback and not method.endswith("Sync"):  # Sync方法没有callback，通过after回调
            self._expose_function(
                method + "_" + super_callback.__name__, super_callback
            )

        return self._evaluate_js(
            "hookWxMethod",
            code_format_info=dict(
                method=method,
                origin=method + "_MiniumOrigin",
                before=method + "_" + super_before.__name__,
                after=method + "_" + super_after.__name__,
                callback=method + "_" + super_callback.__name__,
            ),
        )

    def release_hook_wx_method(self, method):
        """
        释放 hook wx 方法
        :param method: 需要释放 hook 的方法
        :return:
        """
        self._evaluate_js(
            "releaseHookWxMethod",
            code_format_info=dict(
                origin=method + "_MiniumOrigin",
                method=method,
                before=method + "_super_before",
                after=method + "_super_after",
                callback=method + "_super_callback",
            ),
        )
        # 移除监听函数
        self.connection.remove(method + "_super_before")
        self.connection.remove(method + "_super_after")
        self.connection.remove(method + "_super_callback")

    def evaluate(self, app_function: str, args=None, sync=False, desc=None):
        """
        向 app Service 层注入代码并执行
        :param app_function:
        :param args:
        :param sync:
        :param desc: 报错描述
        :return:
        """
        return self._evaluate(
            app_function=app_function, args=args, sync=sync, desc=desc
        )

    # protect method

    def hook_current_page_method(self, method, callback):
        """
        hook 当前页面的方法
        :param method:  方法名
        :param callback:    回调函数
        """

        def super_callback(msg):
            self.logger.debug(f"Page.{method} call hook result: {msg['args']}")
            if callback:
                callback(msg["args"])

        if callback and not callable(callback):
            self.logger.error(f"Page.{method} hook callback method is non-callable")
            return
        if callback:
            self._expose_function(
                "page_hook_" + method + "_" + super_callback.__name__, super_callback
            )
        self._evaluate_js(
            "hookCurrentPageMethod",
            code_format_info={
                "method": method,
                "callback": "page_hook_" + method + "_" + super_callback.__name__,
            },
        )

    def release_hook_current_page_method(self, method):
        # 移除监听函数
        self.connection.remove("page_hook_" + method + "_super_callback")

    # private method

    def _wait(self, func, timeout, interval=1):
        """
        等待直到`func`为true
        :func: callable function
        :timeout: timeout
        :interval: query step
        :return: bool
        """
        # func = lambda :True or False
        if not callable(func):
            return False
        s = time.time()
        timeout = timeout or interval
        while time.time() - s < timeout:
            if func():
                return True
            time.sleep(interval)
        return False

    def _call_wx_method(self, method, args=None, plugin_appid=None):
        if args is None:
            args = []
        if not isinstance(args, list):
            if isinstance(args, str):
                # 如果是字符型参数，就可以不用管是否是 sync 方法，直接转数组传参即可
                args = [args]
            elif "Sync" in method:
                # 如果是 sync 方法，则需要从字典里面提取所有的 value 成为一个数组进行传参
                if isinstance(args, dict):
                    temp_args = list()
                    for key in args.keys():
                        temp_args.append(args[key])
                    args = temp_args
            else:
                # 异步方法的话无需管 args 是str 还是 dict，直接转成 list 即可
                args = [args]

        params = {"method": method, "args": args}
        if plugin_appid:
            params["pluginId"] = plugin_appid
        return self.connection.send("App.callWxMethod", params)

    def _evaluate(self, app_function: str, args=None, sync=False, desc=None):
        if not args:
            args = []
        if sync:
            return self.connection.send(
                Command(
                    "App.callFunction",
                    {"functionDeclaration": app_function, "args": args},
                    desc=desc,
                )
            )
        else:
            return self.connection.send_async(
                "App.callFunction", {"functionDeclaration": app_function, "args": args}
            )

    def _evaluate_js(
        self,
        filename,
        args=None,
        sync=True,
        default=None,
        code_format_info=None,
        mode=None,
        **kwargs,
    ):
        """
        运行 js 代码
        :param filename: {JS_PATH} 中 JS 文件名字（不需要后缀）
        :param code_format_info: JS 内容中需要进行格式化的信息, 如内容中包含 `%s` `%(arg)s` 等的可格式化信息
        :param args: 注入函数需要输入的参数列表
        :param sync: 同步执行函数
        :param mode: js mode: 仅支持es5还是都支持
        :param default: 同步结果返回默认值
        """
        if args is None:
            args = []
        ret = self._evaluate(
            getInjectJsCode(filename, format_info=code_format_info, mode=mode),
            args,
            sync=sync,
            **kwargs,
        )
        if sync:
            return ret.get("result", {}).get("result", default)
        return ret

    def _get_async_response(self, msg_id: str):
        return self.connection.get_aysnc_msg_return(msg_id)

    def _expose_function(self, name, binding_function):
        self.connection.register(name, binding_function)
        self.connection.send("App.addBinding", {"name": name})

    def _unregister(self, name, binding_function=None):
        self.connection.remove(name, binding_function)

    def _mock_wx_method(
        self,
        method,
        functionDeclaration: str="",
        result=None,
        args=None,
        success=True,
        plugin_appid=None,
    ):
        if not args:
            args = []
        elif not isinstance(args, tuple):
            args = [args]
        callback_type = "ok" if success else "fail"
        params = {"method": method}
        if plugin_appid:
            params["pluginId"] = plugin_appid
        if functionDeclaration:
            params.update({"functionDeclaration": functionDeclaration, "args": args})
        elif isinstance(result, str):
            params["result"] = {
                "result": result,
                "errMsg": "%s:%s" % (method, callback_type),
            }
        elif isinstance(result, dict):
            params["result"] = result
        else:
            self.logger.warning("mock wx method accept str or dict result only")
            return
        return self.connection.send("App.mockWxMethod", params)

    def _mock_wx_js(
        self, method, filename, args=None, code_format_info=None, plugin_appid=None
    ):
        """
        mock方法中定义的替换函数直接返回一个promise, promise不需要reject, 自动化协议会根据回调的errmsg来判断回调success/fail
        """
        return self._mock_wx_method(
            method,
            getInjectJsCode(filename, format_info=code_format_info),
            args=args,
            plugin_appid=plugin_appid,
        )
