#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: lockerzhang
@LastEditors: lockerzhang
@Description: 小程序层面的操作(包含 web 和 Native)
@Date: 2019-03-11 14:41:43
@LastEditTime: 2019-06-05 16:30:44
"""
import typing
from enum import Enum
from .page import Page
from .minium_object import MiniumObject
from ...framework.exception import *
from ...utils.injectjs import getInjectJsCode, JsMode
from ...utils.platforms import *
import os
import json
import threading
import base64
import io
import time
import datetime
import copy

try:
    import urllib as urlencoder

    urlencoder.urlencode
except (ImportError, AttributeError):
    import urllib3.request as urlencoder

cur_path = os.path.dirname(os.path.realpath(__file__))  # source_path是存放资源文件的路径
conf_path = os.path.join(os.path.dirname(cur_path), "conf/iOS_conf")


class MockNetworkType(Enum):
    ALWAYS = 0
    ONCE = 1

class MockCloudCallType(Enum):
    ALWAYS = 0
    ONCE = 1


class App(MiniumObject):
    def __init__(self, connection, relaunch=False, native=None, platform="ide"):
        """
        创建一个 APP 实例
        :param connection:
        """
        super().__init__()
        self.connection = connection
        self.native = native
        self.platform = platform
        self.js_mode: JsMode = JsMode.JUST_ES5 if platform in [OS_ANDROID, OS_IOS] else JsMode.ALL  # 真机调试2.0环境下只支持es5语法
        self._msg_lock = threading.Condition()
        self._is_log_enable = False
        self.main_page_path = None
        self.route_return_page = None
        self.route_return_page_update_time = None  # 监听到页面变化后由于是异步通信, 有可能出现两个相近信息重复顺序调乱
        self._appid = None
        self._current_page = None  # 只有调用 get_current_page 和 监听到 _on_route_changed 回调时更新
        self._mocked_images = None
        self._mocked_images_dir = None
        self._mocked_images_data = {}
        # init methods
        self._route_change_listener()
        self._request_stack_listener()
        self.__is_injected = self._evaluate_js(
            "checkInject"
        )  # 是否已经注入过了, 注入过的环境不需要重复注入, 防止出现多次回调等预期之外的情况
        if not self.__is_injected and self.js_mode is JsMode.JUST_ES5:  # 注入一些垫片
            self._evaluate_js(
                "helpers"
            )
        if relaunch:
            self.go_home()

    @property
    def app_id(self):
        if not self._appid:
            self._appid = self._get_account_info_sync().result.result.miniProgram.appId
        return self._appid

    @property
    def current_page(self):
        return self._current_page or self.get_current_page()

    @property
    def is_injected(self):
        """
        是否已经注入过, 如果没有, 则设置并进行注入操作
        """
        if self.__is_injected:
            return True
        self.__is_injected = True
        return False

    def _evaluate_js(
        self,
        filename,
        args=None,
        sync=True,
        default=None,
        code_format_info=None,
        **kwargs,
    ):
        """
        重写, 默认使用self.js_mode参数
        """
        return super(App, self)._evaluate_js(
           filename,
           args,
           sync,
           default,
           code_format_info,
           self.js_mode,
           **kwargs 
        )

    def enable_log(self):
        """
        打开日志
        每次调用, 都会新增一个回调, 最好记录一下已经调用过
        """
        if not self._is_log_enable:
            self.connection.send("App.enableLog")
            self._is_log_enable = True

    def exit(self):
        """
        退出小程序
        :return: None
        """
        self.connection.send("App.exit")

    def get_account_info_sync(self):
        """
        获取账号信息
        :return:
        """
        return self._get_account_info_sync()

    def screen_shot(self, save_path=None, format="raw", use_native=False):
        """
        截图, 仅能截取 webview 部分, 原生控件不能截取到
        :param save_path:
        :param format: raw or pillow
        :param use_native: use native interface
        :return:
        """
        if self.platform != "ide":
            # 小程序不是运行在开发者工具中, 不支持`App.captureScreenshot`
            if self.native:
                # 使用native接口实现截图
                _save_path = save_path or "%s.png" % datetime.datetime.now().strftime(
                    "%H%M%S%f"
                )
                self.native.screen_shot(_save_path)
                if not os.path.isfile(_save_path):
                    self.logger.error("%s.screen_shot fail" % self.native.__class__)
                    return None
                with open(_save_path, "rb") as fd:
                    raw_value = fd.read()
                if not save_path:
                    os.remove(_save_path)
        else:
            try:
                b64_data = (
                    self.connection.send("App.captureScreenshot")
                    .get("result")
                    .get("data")
                )
            except MiniAppError as e:
                self.logger.error(e)
                return None
            else:
                raw_value = base64.b64decode(b64_data)
                png_header = b"\x89PNG\r\n\x1a\n"
                if not raw_value.startswith(png_header) and save_path:
                    self.logger.error("screenshot png format error")

                if save_path:
                    with open(save_path, "wb") as f:
                        f.write(raw_value)

        if format == "raw":
            return raw_value
        elif format == "pillow":
            from PIL import Image

            buff = io.BytesIO(raw_value)
            return Image.open(buff)
        else:
            self.logger.warning(f"unknown format:{format} for screenshot")
            return raw_value

    def expose_function(self, name, binding_function):
        """
        在 AppService 全局暴露方法, 供小程序侧调用测试脚本中的方法。
        :param name:
        :param binding_function:
        :return:
        """
        self._expose_function(name, binding_function)

    def add_observer(self, event, callback):
        """
        监听小程序的事件
        :param event: 需要监听的事件
        :param callback: 收到事件后的回调函数
        :return:
        """
        if not callable(callback):
            raise Exception("the callback is not a function")

        self.connection.register(event, callback)

    def remove_observer(self, event, callback=None):
        """
        移除小程序事件监听
        :param event: 监听的事件
        :param callback: 指定的监听函数, 不传则移除该事件所有监听函数
        :return:
        """
        self.connection.remove(event, callback)

    def on_exception_thrown(self, func):
        """
        JS 错误回调
        :param func: 回调函数
        :return:
        """
        self.connection.register("App.exceptionThrown", func)

    def call_wx_method(self, method, args=None, plugin_appid="auto"):
        """
        调用 wx 的方法
        :param method:
        :param args:
        :param plugin_appid: 调用插件[${appid}]中的方法, auto时自动获取当前页面是否插件页
        :return:
        """
        if plugin_appid == "auto":
            plugin_appid = (self._current_page or self.get_current_page()).plugin_appid
        return self._call_wx_method(method=method, args=args, plugin_appid=plugin_appid)

    def get_all_pages_path(self):
        """
        获取所有已配置的页面路径
        :return:
        """
        return self._evaluate_js("getAllPagesPath")

    def get_current_page(self) -> Page:
        """
        获取当前顶层页面
        :return: Page 对象
        """

        def get_current_page(cnt=0):
            ret = self.connection.send("App.getCurrentPage")
            if hasattr(ret, "error"):
                raise Exception("Get current page fail, cause: %s" % ret.error)
            if not ret.result and cnt < 3:
                # 返回信息有问题, 没拿到pageId等属性
                return get_current_page(cnt + 1)
            return ret

        ret = get_current_page()
        page = Page(
            ret.result.pageId, ret.result.path, ret.result.query, self.connection
        )
        # 记录当前页面
        self._current_page = page
        return page

    def get_page_stack(self) -> typing.List[Page]:
        """
        获取当前小程序所有的页面
        :return: Page List
        """
        ret = self.connection.send("App.getPageStack")
        page_stack = []
        for page in ret.result.pageStack:
            page_stack.append(Page(page.pageId, page.path, page.query, self.connection))
        return page_stack

    def navigate_to(self, url, params=None, is_wait_url_change=True):
        """
        以导航的方式跳转到指定页面, 但是不能跳到 tabbar 页面。支持相对路径和绝对路径, 小程序中页面栈最多十层
        支持相对路径和绝对路径
        /page/tabBar/API/index: 绝对路径,最前面为/
        tabBar/API/index: 相对路径, 会被拼接在当前页面的路径后面
        :param url:"/page/tabBar/API/index"
        :param params: 页面参数
        :param is_wait_url_change: 是否等待页面变换完成
        :return:Page 对象
        """
        if params:
            url += (
                ("?" + urlencoder.urlencode(params))
                if url.find("?") < 0
                else ("&" + urlencoder.urlencode(params))
            )
        self.logger.info("NavigateTo: %s" % url)
        page = self._change_route("navigateTo", url, is_wait_url_change)
        if page.path != url.split("?")[0]:
            self.logger.warning("NavigateTo(%s) but(%s)" % (url, page.path))
        return page

    def redirect_to(self, url, params=None, is_wait_url_change=True):
        """
        关闭当前页面, 重定向到应用内的某个页面。但是不允许跳转到 tabbar 页面
        :param url:"/page/tabBar/API/index"
        :param params: 页面参数
        :param is_wait_url_change: 是否等待页面变换完成
        :return:Page 对象
        """
        if params:
            url += (
                ("?" + urlencoder.urlencode(params))
                if url.find("?") < 0
                else ("&" + urlencoder.urlencode(params))
            )
        self.logger.info("RedirectTo: %s" % url)
        page = self._change_route("redirectTo", url, is_wait_url_change)
        if page.path != url.split("?")[0]:
            self.logger.warning("RedirectTo(%s) but(%s)" % (url, page.path))
        return page

    def relaunch(self, url, params=None, is_wait_url_change=True):
        """
        关闭所有页面, 打开到应用内的某个页面
        :param url: "/page/tabBar/API/index"
        :return:Page 对象
        """
        if params:
            url += (
                ("?" + urlencoder.urlencode(params))
                if url.find("?") < 0
                else ("&" + urlencoder.urlencode(params))
            )
        self.logger.info("ReLaunch: %s" % url)
        page = self._change_route("reLaunch", url, is_wait_url_change)
        if page.path != url.split("?")[0]:
            self.logger.warning("ReLaunch(%s) but(%s)" % (url, page.path))
        return page

    def navigate_back(self, delta=1):
        """
        关闭当前页面, 返回上一页面或多级页面。
        :param delta: 返回的层数, 如果超出 page stack 最大层数返回首页
        :return:Page 对象
        """
        # self._wait_until_page_is_stable()
        page = self.current_page
        page_stack = self._page_stack()
        if page.page_id == page_stack[0].page_id:
            self.logger.warning("Current page is root, can't navigate back")
            return page
        self.logger.info("NavigateBack from:%s" % page.path)
        self._call_wx_method("navigateBack", [{"delta": delta}])
        if self._route_changed():
            return self.route_return_page
        else:
            self.logger.warning("route has not change, may be navigate back fail")

    def switch_tab(self, url, is_wait_url_change=True):
        """
        跳转到 tabBar 页面, 并关闭其他所有非 tabBar 页面
        :param url: "/page/tabBar/API/index"
        :return:Page 对象
        """
        page = self._change_route("switchTab", url, is_wait_url_change)
        if page.path != url.split("?")[0]:
            self.logger.warning("Switch tab(%s) but(%s)" % (url, page.path))
        return page

    def stop_audits(self, path: str = None):
        """
        停止体验测评
        :path: 存放评测结果html的路径, 默认不存
        :return: dict, 测评结果
        """
        ret = self._stop_audits()
        if path:
            html_result = ret["result"]["report"]
            with open(path, "w", encoding="utf-8") as h_f:
                h_f.write(html_result)
        return json.loads(ret["result"]["data"])

    def get_perf_time(self, entry_types: list = None):
        default_entry_types = ["render", "script", "navigation", "loadPackage"]
        if not entry_types:
            entry_types = default_entry_types
        for item_type in entry_types:
            if item_type not in default_entry_types:
                raise Exception("the entryType is not available")
        self._evaluate_js(
            "startGetPerformance",
            [
                entry_types,
            ],
        )

    def stop_get_perf_time(self):
        time.sleep(2)  # 收集数据的时间推后一点点, 怕收集不完全
        return self._evaluate_js("stopGetPerformance")

    def go_home(self, main_page_path=None):
        """
        跳转到首页
        :param main_page_path: 路径
        :return: Page 对象
        """
        if not main_page_path:
            if self.main_page_path:
                main_page_path = self.main_page_path
            else:
                main_page_path = (
                    "/" + self._get_launch_options_sync().result.result.path
                )
                if main_page_path == "/":
                    raise MiniLaunchError("get launch options failed")
                self.main_page_path = main_page_path

        page = self.relaunch(main_page_path)
        return page

    def get_async_response(self, msg_id: str, timeout=None) -> None or dict:
        """
        description: 获取异步调用的结果
        param {*} self
        param {str} msg_id 消息ID
        param {int} timeout 超时时间
        return {*}
        """
        if timeout is None:
            return self._get_async_response(msg_id)
        ret = None

        def get():
            nonlocal ret
            ret = self._get_async_response(msg_id)
            return ret is not None

        self._wait(get, timeout)
        return ret

    def wait_for_page(self, page_path=None, max_timeout=10):
        if not self._current_page or self._current_page.path != page_path:
            # 没有记录到当前页面/当前页面不是目标页面, 等待页面跳转成功的回调
            self._msg_lock.acquire()
            ret = self._msg_lock.wait(max_timeout)
            self._msg_lock.release()
            if not ret:
                current_page = self.get_current_page()
                return current_page.path == page_path
            return ret
        return True

    def wait_util(self, cnt, max_timeout=10):
        """
        {max_timeout}秒内, 剩余没有完成的请求数 <= {cnt}个
        符合上述条件则返回 True, 否则 False
        """
        return self._evaluate_js("waitUtil", [cnt, max_timeout], default=False)

    def _get_launch_options_sync(self):
        return self._call_wx_method("getLaunchOptionsSync")

    def _change_route(self, open_type, path, is_wait_url_change=True):
        self.call_wx_method(open_type, [{"url": path}])
        if self._route_changed():
            return self.route_return_page
        else:
            return self.current_page  # todo: 状态有BUG, 超时也认为可用的

    def _on_route_changed(self, message):
        if not message.name == "onAppRouteDone":
            return
        args = message.args
        options = args[0]
        update_time = args[1] if len(args) > 1 else int(time.time() * 1000)
        if (
            self.route_return_page_update_time
            and self.route_return_page_update_time > update_time
        ):
            # 旧信息, 丢弃
            return
        self.route_return_page = Page(
            options.webviewId, options.path, options.query, self.connection
        )
        # 记录当前页面
        self._current_page = self.route_return_page
        self._msg_lock.acquire()
        self._msg_lock.notify()
        self._msg_lock.release()
        self.logger.info("Route changed, %s" % message)

    def _route_changed(self, timeout=None):
        if not timeout:
            timeout = 5

        self._msg_lock.acquire()
        ret = self._msg_lock.wait(timeout)
        self._msg_lock.release()
        return ret

    # def _inject_global(self):
    #     self._evaluate("""function() {
    #         if (typeof global === "undefined") {
    #             global = (function() {
    #                 return this;
    #             })();
    #             if (typeof window === "object") global = window;
    #         }
    #     }""")

    def _route_change_listener(self):
        self._unregister("onAppRouteDone")
        self._expose_function("onAppRouteDone", self._on_route_changed)
        self._evaluate(
            """function () {
    if (!global.__minium_onAppRouteDone) {
        wx.onAppRouteDone(function (options) {
            onAppRouteDone(options, Date.now())
        })
        global.__minium_onAppRouteDone = true
    }
}""",
            sync=True,
        )

    def _request_stack_listener(self):
        return self._evaluate_js("requestStack")

    def _get_account_info_sync(self):
        return self._call_wx_method("getAccountInfoSync")

    def _page_stack(self):
        ret = self.connection.send("App.getPageStack")
        page_stack = []
        for page in ret.result.pageStack:
            page_stack.append(Page(page.pageId, page.path, page.query, self.connection))
        return page_stack

    def _stop_audits(self):
        ret = self.connection.send("Tool.stopAudits")
        return ret

    ###
    # 各类 mock
    ###

    def _mock_network(
        self,
        interface: str,
        rule: str or dict,
        success=None,
        fail=None,
        mock_type=MockNetworkType.ALWAYS,
    ):
        if success and fail:
            raise RuntimeError("Can't call back both SUCCESS and FAIL")
        if not (success or fail):
            raise RuntimeError("Must call back either SUCCESS or FAIL")
        if isinstance(rule, (str, bytes)):
            # 默认匹配url
            _rule = {"url": rule}
        else:
            _rule = rule
        if success:
            _rule["success"] = success
        elif fail:
            if isinstance(fail, (str, bytes)):
                fail = {"errMsg": "%s:fail %s" % (interface, fail)}
            _rule["fail"] = fail
        if mock_type == MockNetworkType.ONCE:
            # 保护字段, 保证不冲突
            _rule["_miniMockType"] = MockNetworkType.ONCE.value
        has_mock = self._evaluate_js(
            "addNetworkMockRule", [_rule], code_format_info={"interface": interface}
        )
        if not has_mock:
            self._evaluate_js("mockNetwork", code_format_info={"interface": interface})

    def _restore_network(self, interface: str):
        """
        恢复被mock的网络接口
        """
        return self._evaluate_js(
            "cleanNetworkMockRule", code_format_info={"interface": interface}
        )

    def _mock_cloud_call(
        self,
        interface: str,
        rule: dict,
        success=None,
        fail=None,
        mock_type=MockCloudCallType.ALWAYS,
    ):
        if success and fail:
            raise RuntimeError("Can't call back both SUCCESS and FAIL")
        if not (success or fail):
            raise RuntimeError("Must call back either SUCCESS or FAIL")
        if not isinstance(rule, dict):
            raise RuntimeError("Cloud call mock rule must be a dict like {\"name\": \"testCloudFunction\"}")
        _rule = copy.deepcopy(rule)
        if success:
            _rule["success"] = success
        elif fail:
            if isinstance(fail, (str, bytes)):
                fail = {"errMsg": "%s:fail %s" % (interface, fail)}
            _rule["fail"] = fail
        if mock_type == MockCloudCallType.ONCE:
            # 保护字段, 保证不冲突
            _rule["_miniMockType"] = MockCloudCallType.ONCE.value
        has_mock = self._evaluate_js(
            "addCloudCallMockRule", [_rule, interface]
        )
        if not has_mock:
            self._evaluate_js("mockCloudCall")

    def _restore_cloud_call(self, interface: str):
        """
        恢复被mock的云调用接口
        """
        return self._evaluate_js(
            "cleanCloudCallMockRule", [interface,]
        )

    def mock_request(self, rule: str or dict, success=None, fail=None):
        """
        mock wx.request, 根据正则mock规则返回mock结果
        """
        return self._mock_network("request", rule, success, fail)

    def mock_request_once(self, rule: str or dict, success=None, fail=None):
        """
        mock wx.request, 根据正则mock规则返回mock结果, 一旦匹配上了, 即废除该rule
        """
        return self._mock_network("request", rule, success, fail, MockNetworkType.ONCE)

    def restore_request(self):
        return self._restore_network("request")

    def mock_call_function(self, rule: dict, success=None, fail=None):
        return self._mock_cloud_call("callFunction", rule, success, fail)

    def mock_call_function_once(self, rule: dict, success=None, fail=None):
        return self._mock_cloud_call("callFunction", rule, success, fail, MockCloudCallType.ONCE)

    def mock_call_container(self, rule: dict, success=None, fail=None):
        return self._mock_cloud_call("callContainer", rule, success, fail)

    def mock_call_container_once(self, rule: dict, success=None, fail=None):
        return self._mock_cloud_call("callContainer", rule, success, fail, MockCloudCallType.ONCE)

    def restore_call_function(self):
        return self._restore_cloud_call("callFunction")

    def restore_call_container(self):
        return self._restore_cloud_call("callContainer")

    def mock_show_modal(self, answer=True):
        """
        mock 弹窗
        :param answer: 默认点击确定
        :return: None
        """
        self._mock_wx_method(
            "showModal",
            result={
                "cancel": answer,
                "confirm": False if answer else True,
                "errMsg": "showModal:ok",
            },
        )

    def mock_get_location(
        self,
        acc=65,
        horizontal_acc=65,
        vertical_acc=65,
        speed=-1,
        altitude=0,
        latitude=23.12908,
        longitude=113.26436,
    ):
        """
        mock 位置获取
        :param acc: 位置的精确度
        :param horizontal_acc: 水平精度, 单位 m
        :param vertical_acc: 垂直精度, 单位 m(Android 无法获取, 返回 0)
        :param speed: 速度, 单位 m/s
        :param altitude: 高度, 单位 m
        :param latitude: 纬度, 范围为 -90~90, 负数表示南纬
        :param longitude: 经度, 范围为 -180~180, 负数表示西经
        :return:
        """
        self._mock_wx_method(
            "getLocation",
            result={
                "accuracy": acc,
                "altitude": altitude,
                "errMsg": "getLocation:ok",
                "horizontalAccuracy": horizontal_acc,
                "verticalAccuracy": vertical_acc,
                "latitude": latitude,
                "longitude": longitude,
                "speed": speed,
            },
        )

    def mock_show_action_sheet(self, tap_index=0):
        """
        mock 显示操作菜单
        :param tap_index: 用户点击的按钮序号, 从上到下的顺序, 从0开始
        :return:
        """
        self._mock_wx_method(
            "showActionSheet",
            result={"errMsg": "showActionSheet:ok", "tapIndex": tap_index},
        )

    def edit_editor_text(self, editorid, text):
        ret = self._evaluate_js(
            "editEditorText",
            code_format_info={
                "editorid": editorid,
                "text": text,
            },
        )
        self.logger.info(ret)
        return ret

    def reflesh_mocked_images(self, mock_images_dir=None, mock_images=None):
        """
        1. 暴露全局方法用于mock chooseImage
        2. 获取已经有的文件列表
        """
        self._mocked_images_dir = mock_images_dir or None
        self._mocked_images_data = mock_images or {}
        if self._mocked_images is None:
            self._mocked_images = {}  # 需要先调用一次reflesh再进行mock
        ret = self._evaluate_js(
            "mockChooseImage",
        )  # [{name, size}]
        if not ret:
            return
        for item in ret:
            self._mocked_images[item["name"]] = item["size"]

    def mock_choose_image(self, name: str, image_b64data: str):
        """
        mock chooseImage, chooseMedia, takePhoto等选择图片相关接口
        :param name: 文件名
        :param image_b64data: base64格式的图片数据
        :return bool: True for success, False for fail
        """
        return self.mock_choose_images([{
            "name": name,
            "b64data": image_b64data
        }])

    def mock_choose_images(self, items):
        """
        mock chooseImage, chooseMedia, takePhoto等选择图片相关接口
        :param items: [{name, b64data} ... ]
            :name: 文件名
            :b64data: base64格式的图片数据
        :return bool: True for success, False for fail
        """
        if self._mocked_images is None:
            self.reflesh_mocked_images()
        ret = self._evaluate_js(
            "evalMockChooseImage",
            [{
                "imageName": item["name"],
                "size": self._mocked_images[item["name"]]
            } if item["name"] in self._mocked_images else {
                "imageName": item["name"],
                "imageData": item["b64data"]
            } for item in items]
        )
        for result in ret:
            self._mocked_images[result["name"]] = result["size"]
        return True

    def mock_choose_image_with_name(self, file_name):
        """
        通过文件名mock上传图片, 被mock的图片需要放在`${mock_images_dir}`或配置在`${mock_images}`键值对中
        :return bool: True for success, False for fail
        """
        if not self._mocked_images_dir and not self._mocked_images_data:
            raise MiniConfigError("can't not use `mock_choose_image`, please config `mock_images_dir` or `mock_images` first")
        if self._mocked_images is None:
            self.reflesh_mocked_images()
        if file_name in self._mocked_images:
            self._evaluate_js(
                "evalMockChooseImage",
                [{
                    "imageName": file_name,
                    "size": self._mocked_images[file_name]
                }]
            )
            return True
        if file_name in self._mocked_images_data:  # 命中data
            file_content = self._mocked_images_data[file_name]
        else:
            file_path = os.path.join(
                self._mocked_images_dir,
                file_name
            )
            if os.path.isfile(file_path):
                with open(file_path, "rb") as fd:
                    c = fd.read()
                    file_content = base64.b64encode(c).decode("utf8")
            else:
                file_content = ""
        if not file_content:
            return False
        ret = self._evaluate_js(
            "evalMockChooseImage",
            [{
                "imageName": file_name,
                "imageData": file_content
            }]
        )
        for result in ret:
            self._mocked_images[result["name"]] = result["size"]
        return True
