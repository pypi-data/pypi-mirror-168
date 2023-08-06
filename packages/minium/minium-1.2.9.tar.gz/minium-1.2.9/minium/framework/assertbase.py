# -*- coding: utf-8 -*-
"""
@author: 'xiazeng'
@created: 2016/11/23
"""
# import unittest
import json
import os.path
import inspect
import time
from .log_color import *
import logging.handlers
import traceback
import datetime
import re
from minium.miniprogram.wx_minium import WXMinium
from .miniconfig import MiniConfig, get_log_level
from minium.framework.libs import unittest

logger = logging.getLogger("minium")
logger.propagate = False
WORKSPACE_DIR = os.path.abspath(os.getcwd())
# print("当前工作路径: %s" % WORKSPACE_DIR)
LOG_FORMATTER = "%(levelname)-5.5s %(asctime)s %(filename)-10s %(funcName)-15s %(lineno)-3d %(message)s"
FILENAME_LOGGER = "loader{0}.log".format(datetime.datetime.now().strftime("%Y%m%d"))

g_console_handler = None
g_case_log_handler = None

g_from_command = False

__ALL__ = ["AssertBase", "exit_when_error"]


def exit_when_error(test_item):
    setattr(test_item, "__stop_when_error", True)
    return test_item


class AssertBase(unittest.TestCase):
    DEVICE_INFO = {}
    CONFIG = None

    test_config: MiniConfig = None

    __hook_assert = False

    def _startTest(self):
        # 初始化配置
        self._setup_config()
        # 初始化hook assert
        self._setup_assert()
        # 初始化日志
        self._setup_log()
        # 初始化结果数据
        self._setup_results()

    def _endTest(self):
        self._teardown_handle()
        self._teardown_collect()
        self._teardown_result()
        self._teardown_log()

    # ===============================================================================================
    # Setup
    # ===============================================================================================
    def _miniSetUp(self):
        # logger.info("_miniSetUp")
        super(AssertBase, self)._miniSetUp()
        if not getattr(
            self, "__skip_mini_init__", None
        ):  # 初始化output需要放在result.starttest中，考虑到不使用miniresult的情况，在case.setup中需要检查一下配置初始化
            self._startTest()

    @classmethod
    def setUpConfig(cls, default=False):
        if cls.CONFIG is None:
            default_config_filename = os.path.join(WORKSPACE_DIR, "config.json")
            if os.path.exists(default_config_filename) and not default:
                logger.info("read config from workspace dir: [%s]" % WORKSPACE_DIR)
                cls.CONFIG = MiniConfig.from_file(default_config_filename)
            else:
                logger.warning("loading default config")
                cls.CONFIG = MiniConfig()
        if cls.CONFIG.outputs is None:
            outputs = os.path.join(os.getcwd(), "outputs")
            if not os.path.exists(outputs):
                os.makedirs(outputs)
            cls.CONFIG.outputs = outputs
        if cls.CONFIG.create_time is None:
            cls.CONFIG.create_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        global g_console_handler, g_case_log_handler
        log_level = get_log_level(cls.CONFIG.debug_mode)
        if g_console_handler is None:  # 格式化 & 染色 -> 屏幕
            console_handler = logging.StreamHandler()
            console_handler.addFilter(colorfilter)
            formatter = logging.Formatter(LOG_FORMATTER)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
            logger.setLevel(log_level)
            g_console_handler = console_handler

        if g_case_log_handler is None:  # 格式化 -> 固化到文件
            log_path = os.path.join(cls.CONFIG.outputs, FILENAME_LOGGER)
            case_log_handler = logging.handlers.RotatingFileHandler(
                log_path, maxBytes=1024 * 1024, encoding="utf-8"
            )
            case_log_handler.addFilter(nofilter)
            formatter = logging.Formatter(LOG_FORMATTER)
            case_log_handler.setFormatter(formatter)
            case_log_handler.setLevel(logging.DEBUG)
            logger.addHandler(case_log_handler)
            logger.setLevel(log_level)
            g_case_log_handler = case_log_handler

        # 每次加载配置都要重新设置日志等级
        logger.setLevel(log_level)

    @classmethod
    def _miniClassSetUp(cls):
        cls.setUpConfig()

    @classmethod
    def setUpClass(cls) -> None:
        if not getattr(cls, "__is_minitest_suite__", False):
            _miniClassSetUp = getattr(cls, "_miniClassSetUp", None)
            if _miniClassSetUp:
                _miniClassSetUp()
        super(AssertBase, cls).setUpClass()

    def _setup_config(self):
        """
        测试结果存放目录
        1.0 版本存放目录
        ${self.test_config.outputs}/${self._testMethodName}/${datetime.datetime.now().strftime("%Y%m%d%H%M%S")}
        2.0 版本存放目录
        ${self.test_config.outputs}/${self.test_config.create_time}/${self._testMethodName}/
        ${datetime.datetime.now().strftime("%Y%m%d%H%M%S")}
        :return:
        """
        self.test_config = MiniConfig(self.CONFIG)
        dt = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        self.test_config.case_output = os.path.join(
            self.test_config.outputs,
            self.test_config.create_time,
            self._testMethodName,
            dt,
        )
        if not os.path.exists(self.test_config.case_output):
            os.makedirs(self.test_config.case_output)

    def _setup_assert(self):
        self.__hook_assert = True
        self._has_assert_error = False
        self.assert_list = []
        self.__assert_index = 0

    def _setup_log(self):
        # 保存日志到outputs
        # case_log_filename = self.wrap_filename("{0}.log".format(self._testMethodName))
        case_log_filename = self.wrap_filename("run.log")
        self._log_filename = os.path.basename(case_log_filename)
        case_log_handler = logging.handlers.RotatingFileHandler(
            case_log_filename, maxBytes=1024 * 1024, encoding="utf-8"
        )
        case_log_handler.addFilter(nofilter)  # 过滤颜色
        case_log_handler.addFilter(kwfilter)  # 过滤无关的关键字
        case_log_handler.addFilter(filefilter)  # 过滤无关的文件log
        formatter = logging.Formatter(LOG_FORMATTER)
        case_log_handler.setFormatter(formatter)
        self._case_log_handler = case_log_handler
        logger.addHandler(self._case_log_handler)
        # logger.info(self.CONFIG)

    def _setup_results(self):
        self.setup_time = time.time()
        self.screen_info = []
        self.check_list = []
        desc = self._testMethodDoc
        if desc is not None:
            lines = desc.split("\n")
            lines = [l.strip() for l in lines if l]
            desc = "\n".join(lines)
        module_filename = inspect.getsourcefile(self.__class__)
        self._test_filename = module_filename
        module_name = None
        if module_filename:
            module_filename = os.sep.join(module_filename.split(".")[:-1])
            tokens = module_filename.split(os.sep)
            if len(tokens) == 1:
                tokens = module_filename.split("/")
            root_package_name = os.path.abspath(__file__).split(os.sep)[-3]
            if root_package_name in tokens:
                index = tokens.index(root_package_name)
                module_name = ".".join(tokens[index + 2:])
            else:
                # 支持启动类不在MMWebTest子目录下
                module_name = ".".join(tokens)
        packages = self.__module__.split(".")
        self.results = {
            "case_name": self._testMethodName,
            "run_time": str(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")),
            "test_type": self.__class__.__name__,
            "case_doc": desc,
            "success": False,
            "failures": "",
            "errors": "",
            "start_timestamp": self.setup_time,
            "is_failure": False,
            "is_error": False,
            "module": module_name,
            "package": ".".join(packages[:-2]) if len(packages) > 2 else packages[0],
            "failed_line_num": -1,
            "device": AssertBase.DEVICE_INFO,
            "log_filename": self._log_filename,
            "error_type": "",
            "error_value": "",
            "error_stages": [],
            "screen_info": self.screen_info,
            "check_list": self.check_list,
            "assert_list": self.assert_list,
        }

    # ===============================================================================================
    # Teardown
    # ===============================================================================================
    def _teardown_handle(self):
        """
        teardown收集数据前进行的操作
        """
        pass

    def _get_error_info(self):
        if not self._outcome:
            logger.error("self._outcome is None, it's not reasonable")
            return getattr(
                self.__class__, "__class_setup_failure_why__", None
            ), getattr(
                self.__class__, "__class_setup_failure_stages__", []
            )  # 看看是不是class失败了
        length = len(self._outcome.errors)
        if length == 1:
            sys_info = self._outcome.errors[-1][-1]
        elif length > 1:
            while length:
                length -= 1
                sys_info = self._outcome.errors[length][-1]
                if sys_info is not None:  # step success
                    return sys_info, getattr(self._outcome, "error_stages", [])
        else:
            sys_info = None
        return sys_info, getattr(self._outcome, "error_stages", [])

    def _teardown_collect(self):
        """
        收集results数据
        """
        self.results["stop_timestamp"] = time.time()
        sys_info, error_stages = self._get_error_info()
        test_method = getattr(self, self._testMethodName)
        source_line = inspect.getsourcelines(test_method)

        if not self.test_config.only_native:
            self.results["appId"] = self.appId
            self.results["appName"] = self.appName
        else:
            logger.warning("Only native mode, skip get APP id and APP nickname")
        self.results["source"] = {"code": source_line[0], "start": source_line[1]}
        if sys_info:
            e_type, e_value, e_traceback = sys_info
            self.results["failed_line_num"] = -1
            stack_lines = traceback.format_exception(e_type, e_value, e_traceback)
            logger.exception(f"{test_method}", exc_info=sys_info)
            if len(stack_lines) > 2:
                r = re.compile(r"File [\'\"](.*)[\'\"], line (\d+), in (\w+)")
                for stack_line in stack_lines[1:]:
                    m = r.search(stack_line)
                    if m:
                        if (
                            m.group(1) == self._test_filename
                            and m.group(3) == self._testMethodName
                        ):
                            self.results["failed_line_num"] = int(m.group(2))
            if self._has_assert_error:
                self.results["failures"] = "".join(stack_lines)
                self.results["is_failure"] = True
            else:
                self.results["errors"] = "".join(stack_lines)
                self.results["is_error"] = True
            self.results["error_type"] = e_type.__name__
            self.results["error_value"] = (
                str(e_value.args[0]) if len(e_value.args) > 0 else ""
            )
            self.results["error_stages"] = error_stages
        else:
            self.results["success"] = True

    def _teardown_log(self):
        """
        落地log
        """
        logger.removeHandler(self._case_log_handler)
        self._case_log_handler.close()

    def _teardown_result(self):
        """
        落地结果数据
        """
        # filename = self.wrap_filename("{0}.json".format(self._testMethodName))
        filename = self.wrap_filename("result.json")
        self.results["filename"] = os.path.basename(filename)
        with open(filename, "w", encoding="UTF-8") as f:
            json.dump(self.results, f, indent=4)

    def _miniTearDown(self):
        # logger.info("_miniTearDown")
        if not getattr(self, "__skip_mini_init__", None):
            self._endTest()

    # ===============================================================================================
    # assert 拦截， 在进行assert开始和拦截之前做一些数据操作
    # ===============================================================================================
    def _add_assert_info(self, name, ret, reason=None):
        self.__assert_index += 1
        try:
            hook_result = self.hook_assert(name, ret, reason)
        except Exception as e:
            logger.exception(e)
            hook_result = None
        self.assert_list.append(
            {
                "name": name,
                "ret": ret,
                "msg": reason,
                **(hook_result if isinstance(hook_result, dict) else {}),
            }
        )

    def __getattribute__(self, item):
        attr = super().__getattribute__(item)
        if item.startswith("assert") and self.__hook_assert and callable(attr):

            def _hook_assert(*args, **kwargs):
                called_frame = inspect.getouterframes(inspect.currentframe(), 2)
                called_name = called_frame[1][3]
                signature = inspect.signature(attr)
                try:
                    msg_index = list(signature.parameters.keys()).index("msg")
                except ValueError:
                    msg_index = -1
                ret = True
                print_msg = None
                try:
                    return attr(*args, **kwargs)
                    # if getattr(type(mgr), "__enter__", None) and getattr(type(mgr), "__exit__", None):  # assertRaise等
                    #     _enter = getattr(type(mgr), "__enter__", None)
                    #     _exit = getattr(type(mgr), "__exit__", None)
                except AssertionError as e:
                    self._has_assert_error = True
                    ret = False
                    print_msg = str(e)
                    raise
                finally:
                    # todo:
                    #  1. msg needed
                    if called_name and not called_name.startswith("assert"):
                        if msg_index < len(args) and msg_index > -1:
                            name = args[msg_index]
                        else:
                            name = kwargs.get("msg")
                        if name:
                            name = re.sub(r"\W|^(?=\d)", "_", name)
                        self._add_assert_info(name or item, ret, print_msg)

            return _hook_assert
        else:
            return attr

    @property
    def screen_dir(self):
        screen_dir = self.wrap_filename("images")
        if not os.path.exists(screen_dir):
            os.makedirs(screen_dir)
        return screen_dir

    def add_screen(self, name, path, url):
        self.screen_info.append(
            {
                "name": name,
                "url": url,
                "path": self.get_relative_path(path),
                "ts": int(time.time()),
                "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    def wrap_filename(self, filename):
        return os.path.abspath(os.path.join(self.test_config.case_output, filename))

    def get_relative_path(self, path):
        output = self.test_config.case_output
        if not os.path.isabs(output):
            output = os.path.abspath(output)
        if not output.endswith(os.path.sep):
            output = output + os.path.sep
        if not os.path.isabs(path):
            path = os.path.abspath(path)
        if not path.startswith(output):
            logger.error("%s not in outputs: %s" % (path, output))
        else:
            path = path[len(output) :]
        return path

    # ===============================================================================================
    # hooks
    # ===============================================================================================
    def hook_assert(self, name, ret, reason=None) -> dict or None:
        """
        在assert校验的时候被调用
        :return: dict
        """
        pass
