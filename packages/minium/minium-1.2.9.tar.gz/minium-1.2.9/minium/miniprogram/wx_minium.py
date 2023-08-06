#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: lockerzhang
@LastEditors: lockerzhang
@Description: client 入口
@Date: 2019-03-11 14:42:52
@LastEditTime: 2019-06-05 15:05:04
"""
import platform
import os
import base64
import json
import re
import threading
from websocket import WebSocketConnectionClosedException

from minium.utils.injectjs import getInjectJsCode, setInjectJsMode
from .base_driver.app import App
from .base_driver.connection import Connection
from .base_driver.minium_object import MiniumObject
from ..framework.miniconfig import MiniConfig, get_log_level
from ..framework.exception import *
from ..native import get_native_driver, BaseNative
from ..utils.utils import isWindows, isMacOS, Version, WaitThread, WaitTimeoutError, add_path_to_env

LOG_FORMATTER = "%(levelname)-5.5s %(asctime)s %(filename)-10s %(funcName)-15s %(lineno)-3d %(message)s"

MAC_DEVTOOL_PATH = "/Applications/wechatwebdevtools.app/Contents/MacOS/cli"
WINDOWS_DEVTOOL_PATH = "C:/Program Files (x86)/Tencent/微信web开发者工具/cli.bat"
TEST_PORT = 9420
UPLOAD_URL = "https://stream.weixin.qq.com/weapp/UploadFile"


class LogLevel(object):
    INFO = 20
    DEBUG_SEND = 12
    METHOD_TRACE = 11
    DEBUG = 9


def build_version():
    config_path = os.path.join(os.path.dirname(__file__), "version.json")
    if not os.path.exists(config_path):
        return {}
    else:
        with open(config_path, "r", encoding="utf8") as f:
            version = json.load(f)
            return version


class WXMinium(MiniumObject):
    """
    自动化入口
    """

    def __init__(
        self,
        conf: MiniConfig = None,
        uri="ws://localhost",
        native: BaseNative = None,
        **kwargs,
    ):
        """
        初始化
        :param uri: WebSocket 地址
        :param conf: 配置
        :param native: native实例
        """
        super().__init__()
        # 私有变量
        self.__wait_for_initialized_time = None  # 等待app.initialized信号的最后时间
        # 公有变量
        if not conf:
            conf = MiniConfig()
        elif isinstance(conf, dict):
            conf = MiniConfig(conf)
        self.conf = conf
        self.logger.setLevel(get_log_level(conf.debug_mode))
        if native is None and conf.device_desire and conf.platform:
            self.native = get_native_driver(conf.platform, conf)
        else:
            self.native = native
        self.version = build_version().get("version", "1.2.0")
        self.sdk_version: Version = Version("0.0.0")
        self.platform = "ide"  # ide, android, ios
        # self.logger.info(self.version)
        self.start_cmd = ""
        self._app = None
        self.connection = None
        test_port = (
            str(conf.test_port) if conf.get("test_port", None) else str(TEST_PORT)
        )
        self.uri = uri + ":" + test_port
        self.test_port = test_port
        self.open_id = conf.get("account_info", {}).get("open_id", None)
        self.ticket = conf.get("account_info", {}).get("ticket", None)
        self.project_path = conf.get("project_path", None)
        self.is_remote = False
        self.is_connected = False
        self.is_audits_running = False  # 体验评分在跑

        self.launch_weapp()

        # 根据配置注入一些必要的代码
        if self.app and not self.app.is_injected:
            self._inject()

    @property
    def app(self) -> App:
        return self._app

    @app.setter
    def app(self, v: App or None):
        if v:
            setInjectJsMode(v.js_mode)  # 每次更新app实例时更新一下
        self._app = v

    def __setup_dev_tool(self):
        if self.conf.get("dev_tool_path", None):  # 配置了cli路径(一定需要是路径), 检查路径是否正确
            if isWindows and not (
                self.conf.dev_tool_path.endswith("cli")
                or self.conf.dev_tool_path.endswith("cli.bat")
            ):
                raise MiniConfigError(
                    "[dev_tool_path] is not correct, it's usually named as 'cli' or 'cli.bat'"
                )
            self.dev_tool_path = self.conf.dev_tool_path
            if not os.path.exists(self.dev_tool_path):
                raise MiniConfigError("[dev_tool_path] is not correct, it should be a absolute path")
        else:  # 检查默认配置
            if isMacOS:
                if os.path.exists(MAC_DEVTOOL_PATH):
                    self.dev_tool_path = MAC_DEVTOOL_PATH
                elif self._do_shell("which cli")[0].strip():  # 看看cli是否已经加到path, 可以直接调用
                    self.dev_tool_path = "cli"
                else:
                    self.logger.warning("default dev_tool_path[%s] not exists and command[cli] not found" % MAC_DEVTOOL_PATH)
                    self.dev_tool_path = None
            elif isWindows:
                if os.path.exists(WINDOWS_DEVTOOL_PATH):
                    # "${WINDOWS_DEVTOOL_PATH}" auto --project xxx --auto-port 9420  ---  有些用户有问题
                    # add path to env, cli.bat auto --project xxx --auto-port 9420  --- 最新使用这种
                    add_path_to_env(os.path.dirname(WINDOWS_DEVTOOL_PATH))
                    self.dev_tool_path = os.path.basename(self.dev_tool_path)
                elif self._do_shell("where cli.bat")[0].strip():  # 看看cli是否已经加到path, 可以直接调用
                    self.dev_tool_path = "cli.bat"
                else:
                    self.logger.warning("default dev_tool_path[%s] not exists and command[cli.bat] not found" % MAC_DEVTOOL_PATH)
                    self.dev_tool_path = None
            else:
                self.logger.warning("Dev tool doesn't support current OS yet")
                self.dev_tool_path = None
        
        # 用到project path的时候一定需要cli path
        if self.project_path and not self.dev_tool_path:
            raise MiniConfigError("dev_tool_path not exists and not config default cli command")

    def __del__(self):
        if self.native and self.conf.auto_authorize:
            self.native.release_auto_authorize()
        self.native = None

    def __getattr__(self, name):
        """
        当minium中方法不存在且native中存在，返回native的方法
        """
        if self.native:
            item = getattr(self.native, name)
            if callable(item):
                return item
        raise AttributeError(
            "'%s' object has no attribute '%s'" % (self.__class__.__name__, name)
        )

    def __wait_app_initialized(self, timeout, signal):
        """
        等待 {signal} 信号, 代表小程序ready了, 可以响应命令了
        """
        self.__wait_for_initialized_time = time.time()
        self.logger.info("wait for [%s], start at %d" % (signal, self.__wait_for_initialized_time))
        ret = self.connection.wait_for(
            method=signal, max_timeout=timeout
        )
        ctime = time.time()
        if not ret and (ctime - self.__wait_for_initialized_time) < timeout:
            # 没有监听到信号，同时等待期间时间有更新
            self.logger.warning("rewait [%s] for %f" % (signal, timeout - (ctime - self.__wait_for_initialized_time)))
            ret = self.connection.wait_for(
                method=signal, max_timeout=timeout - (ctime - self.__wait_for_initialized_time)
            )
        return ret

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
        重写, 默认使用self.app.js_mode参数
        """
        return super(WXMinium, self)._evaluate_js(
           filename,
           args,
           sync,
           default,
           code_format_info,
           self.app.js_mode,
           **kwargs 
        )

    def _inject(self):
        # IdeNative实例有mini属性，因为IdeNative接口通过minium实现
        if (
            self.platform == "ide"
            and self.native
            and hasattr(self.native, "mini")
            and not self.native.mini
        ):
            self.native.mini = self
        # conf.mock_native_modal
        if self.platform == "ide" and isinstance(
            self.conf.mock_native_modal, dict
        ):  # IDE上不支持原生接口, 用特殊方法mock
            # mini_auth_setting: 记录MOCK过的授权窗，如果确认过授权，后面不需要再通过handle来点击;
            # mock_native_modal_list: 回调栈;
            # handle_mock_native_modal: 弹窗操作;
            # handle_mock_map_modal: 地图操作;
            # mock_native_modal: 添加回调栈;
            # mock_map_modal: 添加地图操作回调栈
            has_mock_native_modal = self._evaluate_js("ideMockModal")
            if not has_mock_native_modal:
                # mock wx.showModal
                self._mock_show_modal()
                # mock wx.showActionSheet
                self._mock_show_action_sheet()
                # mock wx.requestSubscribeMessage
                self._mock_request_subscribe_message()
                # 授权相关接口需要先获取SETTING
                mini_setting = (
                    self.app.call_wx_method("getSetting")
                    .get("result", {})
                    .get("result")
                )
                # 获取到原始setting，mock这个接口
                self.app._mock_wx_js("getSetting", "ideMockAuthSetting")
                # 因为不是真正授权了，只能返回一个假的授权状态
                self.app._mock_wx_js("authorize", "ideMockAuth")
                # mock wx.getLocation，先看看是否有`scope.userLocation`权限，如果已有，则不需要MOCK
                if (
                    mini_setting["authSetting"].get("scope.userLocation") is None
                ):  # 没有授权，mock掉使之不弹窗
                    self._mock_get_location(
                        self.conf.mock_native_modal.get("location", {})
                    )
                # mock wx.chooseLocation, 授权过获取位置也应该mock掉，不然会弹窗
                if mini_setting["authSetting"].get("scope.userLocation") in (
                    None,
                    True,
                ):
                    self._mock_choose_location(
                        self.conf.mock_native_modal.get("location", {}),
                        self.conf.mock_native_modal.get("locations", {}),
                    )
                # mock getWeRunData, 没有授权，mock掉使之不弹窗, 返回的参数由于有加密信息，直接mock数据会导致后面后台解密过不去，需要添加配置来输入MOCK数据
                if mini_setting["authSetting"].get("scope.werun") is None:
                    self._mock_get_we_run_data(
                        self.conf.mock_native_modal.get("weRunData", {}).get(
                            "encryptedData", "testencryptedData"
                        ),
                        self.conf.mock_native_modal.get("weRunData", {}).get(
                            "iv", "testiv"
                        ),
                    )
                # mock getUserProfile, 基础库2.10.4后才支持
                if self.sdk_version >= Version("2.10.4"):
                    self._mock_get_user_profile(
                        self.conf.mock_native_modal.get("userInfo", {})
                    )

        # conf.mock_request
        if self.conf.mock_request and isinstance(self.conf.mock_request, (list, tuple)):
            for item in self.conf.mock_request:
                try:
                    self.app.mock_request(**item)
                except Exception as e:
                    self.logger.exception(
                        "mock_request config error, configure item is %s, error is %s"
                        % (str(item), str(e))
                    )

        # conf.auto_authorize
        if self.conf.auto_authorize and self.native:  # 需要native实例来处理
            self._set_auto_authorize()

        # conf.mock_images_dir
        # 需要进行mock的图片放置的文件夹
        # conf.mock_images
        # 需要进行mock的图片的kv对
        if self.conf.mock_images_dir or self.conf.mock_images:
            # mockChooseImage
            self.app.reflesh_mocked_images(self.conf.mock_images_dir, self.conf.mock_images)

    def _set_auto_authorize(self):
        self.native.set_auto_authorize()
        # hook 可能引起弹窗的函数: authorize, getLocation, chooseLocation, getWeRunData, getUserProfile
        def notify(*args):
            self.native.notify()

        self.app.hook_wx_method("authorize", after=notify)
        self.app.hook_wx_method("getLocation", after=notify)
        self.app.hook_wx_method("chooseLocation", after=notify)
        self.app.hook_wx_method("getWeRunData", after=notify)
        self.app.hook_wx_method("getUserProfile", after=notify)
        notify()  # 小程序可能刚起来就会有授权弹窗

    def _mock_show_modal(self):
        """
        mock showModal, 不弹窗, 但可以用native方法调用
        """
        self.app._mock_wx_js("showModal", "ideMockShowModal")

    def _mock_show_action_sheet(self):
        """
        mock showActionSheet, 不弹窗, 但可以用native方法调用
        """
        self.app._mock_wx_js("showActionSheet", "ideMockShowActionSheet")

    def _mock_request_subscribe_message(self):
        """
        mock requestSubscribeMessage, 不弹窗, 但可以用native方法调用
        """
        self.app._mock_wx_js("requestSubscribeMessage", "ideMockSubscribeMessage")

    def _mock_get_location(self, location=None):
        """
        mock getLocation, 不弹窗, 但可以用native方法调用
        """
        if location is None:
            location = {}
        self.app._mock_wx_js("getLocation", "ideMockGetLocation", location)

    def _mock_choose_location(self, location, locations):
        """
        mock chooseLocation, 不弹窗, 但可以用native方法调用
        """
        self.app._mock_wx_js("chooseLocation", "ideMockChooseLocation", (location, locations))

    def _mock_get_we_run_data(self, encrypted_data, iv):
        """
        mock getWeRunData, 不弹窗, 但可以用native方法调用
        """
        self.app._mock_wx_js("getWeRunData", "ideMockGetWeRunData", (encrypted_data, iv))

    def _mock_get_user_profile(self, user_info):
        """
        mock getUserProfile, 不弹窗, 但可以用native方法调用
        """
        self.app._mock_wx_js("getUserProfile", "ideMockGetUserProfile", user_info)

    def _dev_cli(self, cmd, input=b""):
        cmd_template = "%s %s"
        # do_shell 返回 output & error, 但是，实际上cli命令out返回的是error message, err返回的是output message
        err, out = self._do_shell(cmd_template % (self.dev_tool_path, cmd), input=input)
        if err:
            # error like:
            # [error] {
            #   code: 10,
            #   message: 'Error: 错误 Error: Port 9422 is in use (code 10)Error: Port 9422 is in use\n' +
            #     '    at Object.exports.auto [as method] (f6d9ab0.js:2:925)\n' +
            #     '    at processTicksAndRejections (node:internal/process/task_queues:93:5)\n' +
            #     '    at async f8c86db.js:2:3593\n' +
            #     '    at async Object.<anonymous> (df8c86db.js:2:2983)'
            # }
            reg = re.search(
                r"(\[error\]\s*{\s*code:\s*(\d+),\s*message:.*(Error:.*\(code\s\d+\)))",
                err,
                re.M,
            )
            if reg:
                # 提取message信息返回
                return reg.group(3)
            return err
        return

    def _get_system_info(self):
        """
        description: 获取当前系统信息，更新platform/sdk_version
        param {*} self
        return {*}
        """
        try:
            system_info = self.get_system_info()
        except MiniTimeoutError:
            # 命令没响应，应该是基础库版本问题
            if self.sdk_version < Version("2.7.3"):
                raise MiniLaunchError("基础库版本[%s]过低，请确认基础库版本>=2.7.3" % self.sdk_version)
            raise
        self.sdk_version = Version(
            system_info.get("SDKVersion", None) or self.sdk_version.version
        )
        platform = system_info.get("platform", "ide").lower()
        self.platform = "ide" if platform == "devtools" else platform

    def launch_weapp(self):
        """
        拉起小程序
        """
        self.__setup_dev_tool()
        self.launch_dev_tool()
        if self.conf.get("platform", None) != "ide":
            path = self.enable_remote_debug(
                use_push=self.conf.get("use_push", True),
                connect_timeout=self.conf.get("remote_connect_timeout", 180),
            )
            self.qr_code = path

    def __update_project_config(self):
        project_config_path = os.path.join(self.project_path, "project.config.json")
        if os.path.isfile(project_config_path):
            conf = {}
            setting = {}
            with open(project_config_path, "r", encoding="UTF-8") as fd:
                j = json.loads(fd.read().strip())
            self.sdk_version = Version(
                j.get("libVersion", "").strip() or self.sdk_version.version
            )
            if self.sdk_version < Version("2.7.3"):  # 尝试fix基础库版本信息
                conf["libVersion"] = "latest"  # latest应该是不合法的
            # update setting
            if j.get("setting", None) is None:
                j["setting"] = {}
            if (
                self.conf.audits is not None
            ):  # 即使工具启动了，修改config.json依然会开始运行体验评分，所以每次launch认为audit running
                setting["autoAudits"] = self.conf.audits
            if conf:  # 需要更新
                j.update(conf)
                j["setting"].update(setting)
                json.dump(j, open(project_config_path, "w", encoding="UTF-8"), indent=2)

    def launch_dev_tool(self):
        # start dev tool with minium model
        self.logger.info("Starting dev tool and launch MiniProgram project ...")
        is_port_in_use = False
        if self.project_path:
            if not os.path.exists(self.project_path):
                raise MiniConfigError("project_path: %s not exists" % self.project_path)
            if not os.path.isdir(self.project_path):
                raise MiniConfigError(
                    "project_path: %s is not directory" % self.project_path
                )
            if not os.path.isfile(
                os.path.join(self.project_path, "project.config.json")
            ):
                raise MiniConfigError(
                    "can't find project.config.json in %s, please confirm the directory contains"
                    " miniproject project" % self.project_path
                )
            self.__update_project_config()
            # config start cmd
            self.start_cmd = 'auto --project "%s" --auto-port %s' % (
                self.project_path,
                self.test_port,
            )
            if self.open_id:
                self.start_cmd += f" --auto-account {self.open_id}"
            elif self.ticket:
                self.start_cmd += f" --test-ticket {self.ticket}"
            # run cmd
            err_msg = self._dev_cli(self.start_cmd, input=b"y")
            if err_msg:
                # launch error
                if "Port %s is in use" % self.test_port in err_msg:
                    # 开发者工具可能已经打开并占用了测试端口, 可直接尝试连接
                    is_port_in_use = True
                else:
                    # 其他错误直接报错看看什么问题
                    raise MiniLaunchError(err_msg)
            else:
                # launch success, wait ide init
                if isWindows:
                    # windows更卡
                    time.sleep(10)
                else:
                    time.sleep(5)
        else:
            self.start_cmd = None
            self.logger.warning(
                "Can not find `project_path` in config, that means you must open dev tool by"
                " automation way first"
            )
            self.logger.warning(
                "If you are not running command like [cli auto --project /path/to/project"
                " --auto-port 9420], you may config `project_path` or run this command first"
            )
            err_msg = None
        try:
            self.connect_dev_tool()
            return
        except MiniConnectError as e:
            # ws连接不上
            self.logger.error(f"{str(e)}, restart now...")
            if is_port_in_use:
                # 端口被占用，先尝试关掉项目再重试
                if self.connection:
                    self.connection.send("Tool.close")
                elif "--auto-account" not in self.start_cmd:
                    self._dev_cli(f'close --project "{self.project_path}"')
                else:
                    raise MiniLaunchError(
                        "In the case with multi-account mode and no connection with dev tool,"
                        " please close devtools by your self"
                    )
                time.sleep(5)
            if self.start_cmd:  # 重启一次
                self.logger.info("Starting dev tool again...")
                err_msg = self._dev_cli(self.start_cmd, input=b"y")
                if err_msg:
                    raise MiniLaunchError(err_msg)
                else:
                    self.logger.info("Restart success")
                    # launch success, wait ide init
                    if isWindows:
                        # windows更卡
                        time.sleep(10)
                    else:
                        time.sleep(5)
                self.connect_dev_tool()
                return
            raise e
        except MiniLaunchError:
            # 初始化app error
            raise

    def connect_dev_tool(self):
        i = 3
        while i:
            try:
                self.logger.info("Trying to connect Dev tool ...")
                connection = Connection(
                    self.uri, timeout=self.conf.get("request_timeout")
                )
                self.connection = connection
                self._get_system_info()
                self.app = App(
                    connection,
                    self.conf.get("auto_relaunch"),
                    native=self.native,
                    platform=self.platform,
                )
            except MiniLaunchError:
                raise
            except Exception as e:
                self.logger.exception(e)
                i -= 1
                if i == 0:
                    raise MiniConnectError(
                        "three times try to connect Dev tool has all fail ..."
                    )
                continue
            else:
                break
        self.is_connected = True
        self.is_audits_running = self.conf.audits
        return True

    def launch_dev_tool_with_login(self):
        # login first
        if not self.dev_tool_path or not os.path.exists(self.dev_tool_path):
            raise MiniConfigError("dev_tool_path: %s not exists" % self.dev_tool_path)
        if isWindows:
            cmd_template = '"%s"  login'
        else:
            cmd_template = "%s login"
        # 需要输出二维码，所以直接用os.system就好了
        ret = os.system(cmd_template % self.dev_tool_path)
        if ret == 0:
            return self.launch_dev_tool()

    def get_app_config(self, *names):
        """
        获取 app 的配置
        :return: object
        """
        return self._evaluate_js("getAppConfig", args=names)

    def get_system_info(self):
        """
        获取系统信息
        :return:
        """
        return (
            self.call_wx_method("getSystemInfoSync")
            .get("result", {"result": {}})
            .get("result", None)
        )

    def enable_remote_debug(self, use_push=True, path=None, connect_timeout=180):
        """
        开启真机调试
        监听信号:
        v1: App.initialized
        v2: Tool.onRemoteDebugConnected
        """
        self.reset_remote_debug()
        time.sleep(2)
        RETRY_TIMES = 3
        if use_push:
            retry_times = RETRY_TIMES
            while retry_times > 0:
                thread1 = None
                thread2 = None
                semaphore = threading.Semaphore(0)  # 用Semaphore标记其中一个信号已到达
                try:
                    thread1 = WaitThread(target=self.__wait_app_initialized, args=(
                        connect_timeout + 30 * (RETRY_TIMES - retry_times), "App.initialized"), semaphore=semaphore)
                    thread1.setDaemon(True)
                    thread1.start()
                    thread2 = WaitThread(target=self.__wait_app_initialized, args=(
                        connect_timeout + 30 * (RETRY_TIMES - retry_times), "Tool.onRemoteDebugConnected"), semaphore=semaphore)
                    thread2.setDaemon(True)
                    thread2.start()
                    self.logger.info(f"Enable remote debug, for the {4 - retry_times}th times")
                    self.connection.send(
                        "Tool.enableRemoteDebug",
                        params={"auto": True},
                        max_timeout=connect_timeout,
                    )
                    self.is_remote = True
                    # 成功发起远程调试后, update一下等待时间
                    self.__wait_for_initialized_time = time.time()
                except Exception as e:
                    retry_times -= 1
                    self.logger.error("enable remote debug fail ...")
                    self.logger.error(e)
                    if retry_times == 0:
                        self.logger.error(
                            "Enable remote debug has been fail three times. Please check your"
                            " network or proxy effective or not "
                        )
                        raise
                    continue
                else:
                    retry_times -= 1
                    ret1 = ret2 = False
                    semaphore.acquire()  # 等待初始化信号
                    if thread1:
                        ret1 = thread1.get_result(block=False) or False
                    if thread2:
                        ret2 = thread2.get_result(block=False) or False
                    if retry_times == 0 and ret1 is False and ret2 is False:
                        self.logger.error(
                            "Wait for APP initialized has been fail three times. Please check your"
                            " phone's current foreground APP is WeChat or not, and check"
                            " miniProgram has been open or not "
                        )
                        raise MiniLaunchError("Launch APP Error")
                    if ret1 is True or ret2 is True:
                        break
                    else:
                        # 等不到App.initialized一般就是白屏，通道不通，exit会报错，跳出重试，需要catch
                        try:
                            self.app.exit()
                        except MiniTimeoutError:
                            # 白屏的时候切换一下扫码编译，有时会有意想不到效果
                            self.connection.send(
                                "Tool.enableRemoteDebug",
                                params={"auto": False},
                                max_timeout=connect_timeout,
                            )
            # 远程调试开启成功后，小程序运行态已经转到手机，需要重新实例化app
            self._get_system_info()
            self.app = App(
                self.connection,
                self.conf.get("auto_relaunch"),
                native=self.native,
                platform=self.platform,
            )
            if not self.app.is_injected:
                self._inject()
            return None
        if path is None:
            path = os.path.join(self.conf.outputs, "debug_qrcode.jpg")
        qr_data = self.connection.send(
            "Tool.enableRemoteDebug", max_timeout=connect_timeout
        ).result.qrCode
        with open(path, "wb") as qr_img:
            qr_img.write(base64.b64decode(qr_data))

        return path

    def reset_remote_debug(self):
        """
        重置远程调试，解决真机调试二维码扫码界面报-50003 等常见错误
        :return:
        """
        return self.connection.send("Tool.resetRemoteDebug")

    def clear_auth(self):
        """
        清除用户授权信息. 公共库 2.9.4 开始生效
        :return:
        """
        if (
            self.conf.mock_native_modal and self.conf.platform == "ide"
        ):  # 对授权弹窗MOCK了，需要清除MOCK信息
            self._evaluate_js("clearMockAuth")
        self.connection.send("Tool.clearAuth")

    def get_test_accounts(self):
        """
        获取已登录的真机账号
        :return: list [{openid, nickName}]
        """
        return self.connection.send("Tool.getTestAccounts").result.accounts

    def shutdown(self):
        """
        关闭 Driver, 释放native引用
        :return: status
        """
        if getattr(self.native, "mini", None):
            self.native.mini = None  # IDE native借用minium通信通道交互
        self.native = None
        try:
            if self.is_remote:
                self.logger.info("MiniProgram closing")
                self.app.exit()
            self.logger.info("Project window closing")
            self.connection.send("Tool.close")
            self._wait(lambda: not self.connection._is_connected, 5, 1)
        except (MiniTimeoutError, MiniAppError) as e:
            self.logger.exception(f"Shutdown Excrption:{e}")

    def stop_audits(self, report_path=None):
        """
        停止体验评分
        """
        if self.is_audits_running and self.app.platform == "ide":  # 仅工具上有意义
            self.logger.info("stopping audits")
            self.is_audits_running = False
            try:
                self.app.stop_audits(
                    report_path
                    or (
                        self.conf.outputs
                        and os.path.join(self.conf.outputs, "audits.html")
                    )
                )
            except (
                MiniTimeoutError,
                MiniAppError,
                WebSocketConnectionClosedException,
            ) as e:
                self.logger.exception(f"Stop audits excrption:{e}")

    def release(self):
        """
        释放所有资源, 不允许在case中调用
        :return: None
        """
        # 停止体验评分, 结果存outputs目录
        self.stop_audits()
        # 释放native
        if getattr(self.native, "mini", None):
            self.native.mini = None  # IDE native借用minium通信通道交互
        native = self.native
        self.native = None
        # 释放app
        if self.is_remote:
            try:
                self.logger.info("MiniProgram closing")
                self.app.exit()
            except (
                MiniTimeoutError,
                MiniAppError,
                WebSocketConnectionClosedException,
            ) as e:
                self.logger.exception(f"Close app excrption:{e}")
            finally:
                if self.app is not None:
                    self.app.native = None
                    self.app = None
        # 释放connection
        try:
            self.connection.send_async("Tool.close")
        except WebSocketConnectionClosedException:
            pass
        finally:
            if self._wait(
                lambda: not self.connection._is_connected, 5, 1
            ):  # already closed
                self.connection.remove_all_observers()
            else:
                self.connection.destroy()
        # 清理一下手机弹窗
        if self.conf.platform != "ide" and native:
            if not native.handle_modal(
                btn_text="确定", title="本地调试已结束", force_title=True
            ):
                native.handle_modal(
                    btn_text="OK", title="Local debugging ended", force_title=True
                )
        native = None


if __name__ == "__main__":

    mini = WXMinium()
