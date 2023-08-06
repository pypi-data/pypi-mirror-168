#!/usr/bin/env python3
# Created by xiazeng on 2019-05-06
import datetime
import json
import os.path
from posixpath import realpath
import shutil
import time
import inspect

import minium
import minium.miniprogram.base_driver.minium_log
import minium.native
from minium.native.exception import *
from .miniconfig import MiniConfig
from .assertbase import AssertBase
from .log_color import *
from .exception import *
from ..utils.utils import retry, catch
from ..utils.injectjs import getInjectJsCode
from .miniprogram import MiniProgram

# import matplotlib.pyplot as plt

logger = logging.getLogger("minium")

g_minium = None
g_native = None
g_log_message_list = []
g_network_message_dict = {}  # 记录请求消息
g_network_req_cache = {}  # 记录请求体消息(降低重复请求消息量)
g_network_resp_cache = {}  # 记录请求返回消息(降低重复请求消息量)


def full_reset():
    """
    在整个测试流程结束之后调用
    1. miniProgram 部分同 reset_minium()
    2. native 部分
        1.1 关闭微信
        1.2 释放原生 driver
    :return:
    """
    global g_minium, g_native
    if g_minium:
        reset_minium()
    if g_native:
        try:
            g_native.stop_wechat()
        except:
            pass
        try:
            g_native.release()
        except:
            pass
        g_native = None


def reset_minium():
    """
    1. miniProgram 部分 release
        1.1 非 ide 运行退出小程序
    2. 释放所有观察者的事件监听
    3. 销毁与 ide 的连接
    :return:
    """
    global g_minium
    g_minium.release()
    g_minium = None


def get_native(cfg: MiniConfig):
    """
    native 部分完全由配置中的 platform 参数控制
    为了确保不会过多地重启微信，已存在 g_native 则不创建,
    teardown 的时候也不会 release
    :param cfg: 配置
    :return:
    """
    global g_native
    if g_native is None:
        g_native = minium.native.get_native_driver(cfg.platform, cfg)
        g_native.start_wechat()
    return g_native


def get_minium(cfg: MiniConfig):
    """
    miniProgram 部分每次 classTearDown 是否 release 由配置 close_ide 控制
    初始化有如下工作：
        1. 处理配置
        2. 如果配置了 project_path 则启动 ide
        3. 连接 ide
        4. 根据配置 platform 判断是否需要远程调试
        5. 根据配置 enable_app_log 判断是否需要监听小程序 log 输出
        6. 根据配置 enable_network_panel 判断是否需要监听小程序 request, downloadFile, uploadFile 输出
    :param cfg: 配置
    :return:
    """
    global g_minium, g_native
    if g_minium is not None and (
        cfg.close_ide or cfg.full_reset
    ):  # 如果是配置了close_ide的，先release minium
        reset_minium()
    if g_minium is None:
        g_minium = minium.miniprogram.get_minium_driver(conf=cfg, native=g_native)

        if not cfg.use_push and cfg.platform != "ide":
            g_native.connect_weapp(g_minium.qr_code)
            ret = g_minium.connection.wait_for(method="App.initialized")
            if ret is False:
                raise MiniAppError("Launch MiniProgram Fail")

        if cfg.enable_app_log:
            g_minium.connection.register("App.logAdded", mini_log_added)
            g_minium.app.enable_log()

        if cfg.enable_network_panel:
            # 没有uuid库，随便注入一个随机ID库
            g_minium.app._evaluate_js("uuid")
            g_minium.app.expose_function("mini_request_callback", request_callback)
            g_minium.app.expose_function("mini_send_request", send_request)
            g_minium.app._evaluate_js("networkPannel")

        if cfg.platform == "ide":
            g_native.mini = g_minium  # ide native接口通过minium实现

    return g_minium


def init_miniprogram(cfg: MiniConfig):
    """
    初始化小程序
    1. 初始化native
    2. 启动微信
    3. 拉起小程序
    4. 获取必要的小程序信息
    """
    logger.info("start init miniprogram")
    native = get_native(cfg)
    mini = get_minium(cfg)
    if cfg.appid and MiniProgram.get_instance(cfg.appid):
        logger.info("miniprogram exists")
        return native, mini, MiniProgram.get_instance(cfg.appid)
    account_info = mini.get_app_config("accountInfo").accountInfo
    system_info = mini.get_system_info()
    appid = ""
    appname = ""
    if account_info:
        appid = account_info.get("appId", "")
        appname = account_info.get("appName", "") or account_info.get(
            "nickname", ""
        )  # 发现appname改成了nickname
    logger.info("end init miniprogram")
    return native, mini, MiniProgram(appid or cfg.appid, appname=appname, system_info=system_info)  # 返回一个默认的

def mini_log_added(message):
    """
    小程序 log 监听回调函数
    将小程序的 log 格式化然后保存起来
    :param message:
    :return:
    """
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message["dt"] = dt
    g_log_message_list.append(message)


def send_request(message):
    [msg_id, obj, ms, hash_id] = message["args"]
    if hash_id and obj:  # 传了原始request obj, 记录起来
        g_network_req_cache[hash_id] = {
            "obj": obj,
            "timestamp": time.time()
        }
    elif hash_id and hash_id in g_network_req_cache:
        obj = g_network_req_cache[hash_id]["obj"]
        g_network_req_cache[hash_id]["timestamp"] = time.time()
    if msg_id not in g_network_message_dict:
        g_network_message_dict[msg_id] = {"timestamp": time.time() * 1000}
    g_network_message_dict[msg_id]["start_timestamp"] = ms
    g_network_message_dict[msg_id]["request"] = json.loads(obj)


def request_callback(message):
    [msg_id, res, ms, hash_id] = message["args"]
    if hash_id and res:  # 传了原始response res, 记录起来
        g_network_resp_cache[hash_id] = {
            "res": res,
            "timestamp": time.time()
        }
    elif hash_id and hash_id in g_network_resp_cache:
        res = g_network_resp_cache[hash_id]["res"]
        g_network_resp_cache[hash_id]["timestamp"] = time.time()
    if msg_id not in g_network_message_dict:
        g_network_message_dict[msg_id] = {"timestamp": time.time() * 1000}
    g_network_message_dict[msg_id]["end_timestamp"] = ms
    g_network_message_dict[msg_id]["response"] = json.loads(res)


class MetaMiniTest(type):
    def __new__(cls, name, bases, attrs):
        cls.app = MetaMiniTest.app
        return super(MetaMiniTest, cls).__new__(cls, name, bases, attrs)

    @property
    def app(cls):
        if not inspect.isclass(cls):
            cls = type(cls)
        return cls._app or (cls.mini and cls.mini.app)

    @app.setter
    def app(cls, value):
        if not inspect.isclass(cls):
            cls = type(cls)
        cls._app = value


class MiniTest(AssertBase, metaclass=MetaMiniTest):
    mini = None
    native = None
    appId = ""
    appName = ""
    logger = logger

    _app = None

    @property
    def app(self) -> minium.App:
        return self._app or (self.mini and self.mini.app)

    @app.setter
    def app(self, value):
        self._app = value

    @classmethod
    def _miniClassSetUp(cls):
        logger.debug("=====================")
        logger.debug("Testing class：%s" % cls.__name__)
        logger.debug("=====================")
        super(MiniTest, cls)._miniClassSetUp()
        if not cls.CONFIG.report_usage:
            minium.miniprogram.base_driver.minium_log.existFlag = 1

        native, mini, miniprogram = init_miniprogram(cls.CONFIG)
        cls.native = native
        cls.mini = mini
        if cls.CONFIG.need_perf:  # start get perf thread
            cls.native.start_get_perf(timeinterval=0.8)
        cls.DEVICE_INFO["system_info"] = miniprogram.system_info

    @classmethod
    def tearDownClass(cls):
        """
        1. 存在 g_minium
        2. 配置 close_ide=True
        3. ide 下不释放
        :return:
        """
        if cls.CONFIG.full_reset:
            logger.info("full reset")
            if cls.CONFIG.audits and cls.mini and hasattr(cls.mini, "stop_audits"):
                cls.mini.stop_audits(
                    os.path.join(cls.CONFIG.outputs, "audits_%s.html" % cls.__name__)
                )
            full_reset()
            return
        if g_minium and cls.CONFIG.close_ide and cls.CONFIG.platform == "ide":
            logger.info("close ide and reset minium")
            if cls.CONFIG.audits and cls.mini and hasattr(cls.mini, "stop_audits"):
                cls.mini.stop_audits(
                    os.path.join(cls.CONFIG.outputs, "audits_%s.html" % cls.__name__)
                )
            reset_minium()

    def _miniSetUp(self):
        super(MiniTest, self)._miniSetUp()
        self._is_perf_setup = False
        self._is_audits_setup = False
        logger.info("=========Current case: %s=========" % self._testMethodName)
        logger.info(
            "package info: %s, case info: %s.%s"
            % (
                self.results.get("module", ""),
                self.__class__.__name__,
                self._testMethodName,
            )
        )
        if self.test_config.only_native:
            logger.info(f"Only native: {self.test_config.only_native}, setUp complete")
            return
        else:
            if self.test_config.auto_relaunch:
                ret = self.native and self.native.back_to_miniprogram()
                if ret and ret != ResetError.OK:
                    if ret == ResetError.RELAUNCH_APP:
                        self.logger.warning(
                            "back_to_miniprogram error, reset app, post native: %s, minium: %s"
                            % (id(self.mini), id(self.native))
                        )
                        full_reset()
                        self.logger.debug(
                            "start init_miniprogram, class is: %s"
                            % self.__class__.__name__
                        )
                        native, mini, miniprogram = init_miniprogram(self.__class__.CONFIG)
                        self.__class__.native = native
                        self.__class__.mini = mini
                        self.logger.debug(
                            "end init_miniprogram, class is: %s"
                            % self.__class__.__name__
                        )
                        self.mini = mini
                        self.native = native
                        self.logger.debug(
                            "finish init_miniprogram, current native: %s, minium: %s"
                            % (id(self.mini), id(self.native))
                        )
                    elif ret == ResetError.RELAUNCH_MINIPROGRAM:
                        self.logger.warning(
                            "back_to_miniprogram error, reset miniprogram, post minium: %s"
                            % id(self.native)
                        )
                        reset_minium()
                        self.logger.debug(
                            "start init_miniprogram, class is: %s"
                            % self.__class__.__name__
                        )
                        native, mini, miniprogram = init_miniprogram(self.__class__.CONFIG)
                        self.__class__.native = native
                        self.__class__.mini = mini
                        self.logger.debug(
                            "end init_miniprogram, class is: %s"
                            % self.__class__.__name__
                        )
                        self.mini = mini
                        self.logger.debug(
                            "finish init_miniprogram, current minium: %s"
                            % id(self.mini)
                        )
                self.app.go_home()
        # 体验评分是个整体的评价，每个case太短了，没意义
        # if self.test_config.audits:
        #     self._is_audits_setup = self._setup_audits()
        if self.test_config.assert_capture:
            retry(2)(self.capture)("setup")
        self._is_perf_setup = self._setup_perf()

    def _setup_perf(self):
        self._get_perf_flag = False
        self.perf_data = ""
        if self.test_config.need_perf:
            # logger.debug("_setup_perf")
            self._get_perf_flag = bool(self.native.start_get_perf(timeinterval=0.8))
        return True

    def _teardown_perf(self):
        """
        落地性能相关数据
        """
        if not self._is_perf_setup:
            return
        perf_init = {
            "startup": self.native.get_start_up(),  # 启动时间
            "avg_cpu": 0,  # 平均CPU
            "max_cpu": 0,  # 最大CPU
            "cpu_data_list": [],  # cpu 数据，可以每3s 打一次
            "avg_mem": 0,  # 平均内存
            "max_mem": 0,  # 最大内存
            "mem_data_list": [],  # 内存数据，可以每3s 打一次
            "avg_fps": 0,  # 平均FPS, 小游戏才有
            "min_fps_rt": 0,  # 最小FPS, 小游戏才有
            "fps_data_list": [],  # FPS数据，可以每3s 打一次
            "fps_time_series_list": [],
            "cpu_time_series_list": [],
            "mem_time_series_list": [],
        }
        if self._get_perf_flag:
            self._get_perf_flag = False
            perf_str = self.native.get_perf_data(self.setup_time)
            if self.native.outputs_screen and os.listdir(self.native.outputs_screen):
                page_path = self.page.path
                for file_name in os.listdir(self.native.outputs_screen):
                    file_name_all = os.path.join(self.native.outputs_screen, file_name)
                    # logger.error(file_name_all)
                    shutil.copy(file_name_all, self.screen_dir)
                    path = os.path.join(self.screen_dir, file_name)
                    # logger.error(path)
                    file_name_noext = os.path.splitext(file_name)[0]
                    self.screen_info.append(
                        {
                            "name": file_name,
                            "url": page_path,
                            "path": self.get_relative_path(path),
                            "ts": int(file_name_noext),
                            "datetime": datetime.datetime.fromtimestamp(
                                int(file_name_noext)
                            ).strftime("%Y-%m-%d %H:%M:%S"),
                        }
                    )
            if not perf_str:
                self.perf_data = json.dumps(perf_init)
            else:
                try:
                    perf_arr = json.loads(perf_str)
                    perf_re = perf_init
                    timestamp_arr = []
                    cpu_arr = []
                    mem_arr = []
                    fps_arr = []
                    fps_time_series_list = []
                    cpu_time_series_list = []
                    mem_time_series_list = []
                    for item in perf_arr:
                        _timestamp = int(item["timestamp"])
                        timestamp_arr.append(_timestamp)
                        if item.get("cpu", None) is not None:
                            cpu_arr.append(int(item["cpu"]))
                            cpu_time_series_list.append(_timestamp)
                        if item.get("fps", None) is not None:
                            fps_arr.append(int(item["fps"]))
                            fps_time_series_list.append(_timestamp)
                        if item.get("mem", None) is not None:
                            mem_arr.append(float(item["mem"]))
                            mem_time_series_list.append(_timestamp)
                    perf_re["fps_time_series_list"] = fps_time_series_list
                    perf_re["cpu_time_series_list"] = cpu_time_series_list
                    perf_re["mem_time_series_list"] = mem_time_series_list
                    perf_re["cpu_data_list"] = cpu_arr
                    perf_re["mem_data_list"] = mem_arr
                    perf_re["fps_data_list"] = fps_arr
                    perf_re["avg_cpu"] = sum(cpu_arr) / (len(cpu_arr) or 1)
                    perf_re["avg_mem"] = sum(mem_arr) / (len(mem_arr) or 1)
                    perf_re["avg_fps"] = sum(fps_arr) / (len(fps_arr) or 1)
                    perf_re["max_cpu"] = max(cpu_arr)
                    perf_re["max_mem"] = max(mem_arr)
                    perf_re["min_fps_rt"] = min(fps_arr)
                    self.perf_data = json.dumps(perf_re)
                except:
                    self.perf_data = json.dumps(perf_init)

        else:
            self.perf_data = json.dumps(perf_init)
        self.results["perf_data"] = self.perf_data

    # 不应在case setup做
    def _setup_audits(self):
        self.audit_html = ""
        self.audit_json = ""
        self.start_audit = False
        if self.test_config.platform == "ide":
            logger.info(f"start run audits score")
            self.start_audit = True
            # 开始执行体验评分用例
        else:
            logger.warn(f"Only ide can run audits score")
        return True

    # 不应在case teardown做
    def _teardown_audits(self):
        """
        落地测评数据
        """
        if not self._is_audits_setup:
            return
        if self.start_audit:
            self.stop_audits()
        self.results["audit_html"] = self.audit_html
        self.results["audit_json"] = self.audit_json

    def _teardown_app_log(self):
        """
        落地小程序相关的log
        """
        global g_log_message_list, g_network_message_dict
        # 落地小程序log
        weapp_path = "weapp.log"
        weapp_filename = self.wrap_filename(weapp_path)
        log_messages = g_log_message_list
        g_log_message_list = []
        with open(weapp_filename, "w", encoding="UTF-8") as f:
            for log_message in log_messages:
                f.write(json.dumps(log_message, ensure_ascii=False) + "\n")
        self.results["weapp_log_path"] = weapp_path

        # 落地网络请求log
        request_path = "request.log"
        request_filename = self.wrap_filename(request_path)
        network_message = g_network_message_dict
        g_network_message_dict = {}
        network_message_list = [network_message[msg_id] for msg_id in network_message]
        network_message_list.sort(
            key=lambda x: x.get("start_timestamp", None) or x["timestamp"]
        )
        with open(request_filename, "w", encoding="UTF-8") as f:
            # msg => {timestamp, start_timestamp, request: dict or None, end_timestamp, response: dict or None}
            for msg in network_message_list:
                # logger.debug("\nrequest: {}\nresponse: {}".format(msg.get("request", "Error: Request None"),
                # msg.get("response", "Error: Response Empty")))
                if not msg.get("start_timestamp"):
                    msg["start_timestamp"] = msg["timestamp"]
                    msg["request"] = None
                if not msg.get("end_timestamp"):
                    msg["end_timestamp"] = msg["timestamp"]
                    msg["response"] = None
                f.write(json.dumps(msg, ensure_ascii=False) + "\n")
        self.results["request_log_path"] = request_path

    def _miniTearDown(self):
        logger.debug("=========Current case Down: %s=========" % self._testMethodName)
        try:
            # 更新小程序专属的数据
            self._teardown_perf()
            # if self.test_config.audits:
            #     self._teardown_audits()
            self._teardown_app_log()
            if self.test_config.assert_capture:
                retry(2)(self.capture)("teardown")
            # todo: 加参数说明是否需要保存页面参数
            if self.test_config.teardown_snapshot:
                self.results["page_data"] = self.page.data
                self.results["page_wxml"] = self.page_wxml
            elif self._outcome:
                sys_info = self._get_error_info()[0]
                if sys_info: # case失败了
                    if sys_info[0] is MiniElementNotFoundError:  # 找不到元素, 把wxml拿回来帮助用户排查
                        self.results["page_wxml"] = self.page_wxml
        except Exception as e:
            logger.exception(e)
            self.results["page_data"] = None
            self.results["page_wxml"] = ""
        finally:
            super(MiniTest, self)._miniTearDown()

    @property
    def page(self) -> minium.Page:
        return self.mini.app.get_current_page()

    @property
    def page_wxml(self) -> str:
        if not self.mini:
            return ""
        if self.mini.sdk_version > "2.19.5":
            wxml = self.page.get_element("/*").outer_wxml
        else:
            wxml = self.page.get_element("page").inner_wxml
        if wxml:
            filename = datetime.datetime.now().strftime("%d%H%M%S.wxml")
            filepath = self.wrap_filename(filename)
            with open(filepath, "w", encoding="utf8") as fd:
                fd.write(wxml)
            return filename
        return wxml

    def capture(self, name=""):
        """
        :param name: 图片名称
        :return: str: image_path or ""
        """
        if name:
            filename = "%s.png" % name
        else:
            filename = "%s.png" % datetime.datetime.now().strftime("%H%M%S%f")
        path = os.path.join(self.screen_dir, filename)
        if os.path.isfile(path):
            # 文件已经存在，重命名
            tmp = os.path.splitext(filename)
            filename = (
                tmp[0] + "_%s" % datetime.datetime.now().strftime("%H%M%S%f") + tmp[1]
            )
            path = os.path.join(self.screen_dir, filename)
        logger.info("capture %s" % filename)
        self.native.screen_shot(path)
        if os.path.exists(path):
            page_path = (
                self.mini.app.route_return_page.path
                if self.mini and self.mini.app.route_return_page
                else ""
            )
            self.add_screen(name, path, page_path)
            return path
        else:
            logger.warning("%s not exists", path)
        return ""

    def stop_audits(self, format=None):
        """
        获取体验评分
        :return: 体验评分报告
        """
        format = ["html", "json"] if format is None else format
        ret = self.app._stop_audits()
        if len(format) == 0:
            raise Exception("未定义format")
        if not "result" in ret:
            raise Exception("stop_audits获取数据为空")
        if not "report" in ret["result"]:
            raise Exception("stop_audits获取html数据为空")
        if not "data" in ret["result"]:
            raise Exception("stop_audits获取json数据为空")

        for item in format:
            if item == "html":
                audits_html_file = "Audits.html"
                audits_htmlname = self.wrap_filename(audits_html_file)
                html_result = ret["result"]["report"]
                with open(audits_htmlname, "w", encoding="utf-8") as h_f:
                    h_f.write(html_result)
                h_f.close()
                self.audit_html = audits_html_file
                logger.info("success create Audits.html")
            elif item == "json":
                audits_json_file = "Audits.json"
                audits_jsonname = self.wrap_filename(audits_json_file)
                json_result = ret["result"]["data"]
                with open(audits_jsonname, "w", encoding="UTF-8") as j_f:
                    j_f.write(json_result)
                j_f.close()
                self.audit_json = audits_json_file
                logger.info("success create Audits.json")
            else:
                pass

    # 小程序定制化的校验
    def assertPageData(self, data, msg=None):
        """

        :param data:
        :param msg:
        :return:
        """
        pass

    def assertContainTexts(self, texts, msg=None):
        pass

    def assertTexts(self, texts, selector="", msg=None):
        for text in texts:
            elem = self.page.get_element(selector, inner_text=text)
            if elem is None:
                raise AssertionError("selector:%s, inner_text=%s not Found")

    def hook_assert(self, name, ret, reason=None):
        if self.test_config.assert_capture:
            filename = "{0}-{1}".format(name, "success" if ret else "failed")
            retry(2)(self.capture)(filename)
            wxml = ""
            if ret is False:
                wxml = self.page_wxml
            return {"img": filename, "wxml": wxml}
