#!/usr/bin/env python3
# Created by xiazeng on 2019-05-22
import os.path
import time

from minium.utils.utils import timeout, wait
from .basenative import BaseNative, NativeError, ResetError, ModalStatus
import at
from at.core.adbwrap import AdbWrap
from at.core.element import Element as ATElement, AtSelector
import at.keycode
import json
import logging
import threading
import shutil
import ssl
import requests
import re
from enum import Enum
from ..lib.android_base import UiDefine, ScreenType

ssl._create_default_https_context = ssl._create_unverified_context

WECHAT_PACKAGE = "com.tencent.mm"
WECHAT_ACTIVITY = "ui.LauncherUI"
MINIPROGRAM_ACTIVITY = "plugin.appbrand.ui.AppBrandUI"
MINIPROGRAM_PLUGIN_ACTIVITY = "plugin.appbrand.ui.AppBrandPluginUI"


logger = logging.getLogger("minium")
_MIN_NORMALIZED_FRAME_LENGTH = 0.5


class ScreenType(Enum):
    AT = 1
    ADB = 2
    WETEST = 3


class WXAndroidNative(BaseNative):
    def __init__(self, json_conf):
        super(WXAndroidNative, self).__init__(json_conf)
        if json_conf is None:
            json_conf = {}
        self.serial = json_conf.get("serial") or AdbWrap.get_default_serial()
        uiautomator_version = int(json_conf.get("uiautomator_version", "2"))
        at.uiautomator_version = uiautomator_version
        self.at = at.At(self.serial)
        self.at.java_driver.set_capture_op(False)
        self.ui = UiDefine(self.at)
        self.lang = json_conf.get("lang")
        self.perf_thread = None
        self.perf_flag = False
        self.ef_able_flag = False
        self.perf_data = []
        self.fps_data_dict = {}  # fps dict
        self.jank_count_dict = {}  # 卡顿次数
        self.fps_thread = None
        self.startup_time = 0
        self.outputs = json_conf.get("outputs") or os.path.dirname(
            os.path.realpath(__file__)
        )
        self.outputs_screen = os.path.join(self.outputs, "image")
        self.screen_type = ScreenType.AT  # 截图方式，默认使用at
        self._empty_base_screen_dir(self.outputs_screen)
        self._current_views = None
        self.pay_modal_version = 0  # 1. 原始版本, 使用计算数字坐标的方式进行点击. 2. 数字按钮具有固定的rid, 格式为: `com.tencent.mm:id/tenpay_keyboard_{number}`

    @property
    def current_views(self):
        if self._current_views is None:
            return self._get_current_views()
        return self._current_views

    @timeout(2, 0.5)
    def _get_current_views(self):
        self._current_views = self.at.java_driver.dump_all_views()
        return self._current_views

    def _el_exist_in_current_view(self, el: ATElement):
        if not self.current_views:
            return False
        instance = el._selector.get(AtSelector.SELECTOR_INSTANCE, 0)
        for ui_view_list in self.current_views:
            for ui_view in ui_view_list:
                if el.match_ui_view(ui_view):
                    if instance == 0:
                        return True
                    else:
                        instance -= 1
        return False

    def _empty_base_screen_dir(self, dirname):
        if os.path.exists(dirname):
            if os.path.isdir(dirname):
                shutil.rmtree(dirname)
                time.sleep(1)
            else:
                os.remove(dirname)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    def _deal_log(self, log):
        log_2 = ""
        log_4 = ""
        for line in log:
            if str(line).find(",StartUp,0") != -1:
                log_1 = str(line).split(",StartUp,0")[0]
                log_2 = str(log_1).split(",")[-1]
                logger.info(log_2)
            elif str(line).find(",StartUp,1") != -1:
                log_3 = str(line).split(",StartUp,1")[0]
                log_4 = str(log_3).split(",")[-1]
                logger.info(log_4)
            else:
                pass

        if log_2 and log_4:
            startup_time = int(log_4) - int(log_2)
            self.startup_time = startup_time
            return startup_time
        else:
            return 0

    @property
    def logcat(self):
        return self.at.logcat

    def connect_weapp(self, path):
        self.at.apkapi.launch()
        gallery_name = "atstub"
        self.at.apkapi.add_gallery(path)
        self.stop_wechat()
        self.start_wechat()
        if self.lang == "en":
            self.e.text("Discover").click()
            self.e.text("Scan").click()
            # self.e.cls_name("android.widget.ImageButton").click()
            # self.e.text("Choose QR Code from Album").click()
            self.e.cls_name("android.widget.LinearLayout").instance(1).click()
            self.e.text("All Images").click()
            self.e.text(gallery_name).click()
            self.e.desc_contains("Image 1").click()
            self.e.text_contains("Scanning").wait_disappear()
        else:
            self.e.text("发现").click()
            self.e.text("扫一扫").click()
            self.e.cls_name("android.widget.LinearLayout").instance(1).click()
            # self.e.cls_name("android.widget.ImageButton").click()
            # self.e.text("从相册选取二维码").click()
            self.e.text("所有图片").click()
            self.e.text(gallery_name).click()
            self.e.desc_contains("图片 1").click()
            self.e.text_contains("扫描中").wait_disappear()

    def screen_shot(self, filename, quality=30):
        """
        安卓截图有两种方式：
        1. via at
        2. via adb screencap
        via at现存问题: 可能因为网络、at进程被kill等问题, 截图时间超长
        """
        if self.screen_type == ScreenType.AT:
            stime = time.time()
            try:
                ret = self.at.device.screen_shot(filename, quality=quality)
            except (requests.ConnectionError, requests.ReadTimeout) as e:
                logger.error("screen_shot error %s, try reconnect" % str(e))
                self.at.java_driver.reconnect()
                stime = time.time()
                ret = self.at.device.screen_shot(filename, quality=quality)
            # ret = self.at.device.screen_shot(filename, quality=quality)
            if time.time() - stime > 50:  # 如果一次截图超过50s, 就切换截图类型
                logger.warning(
                    "screen_shot cost bigger than 50s, change the screen type"
                )
                self.screen_type = ScreenType.ADB
            return ret
        elif self.screen_type == ScreenType.ADB:
            return self.at.device.screen_shot(filename, quality=quality, display_id=0)

    def pick_media_file(
        self,
        cap_type="camera",
        media_type="photo",
        original=False,
        duration=5.0,
        index_list=None,
    ):
        pass

    def input_text(self, text):
        """ """
        self.at.e.edit_text().enter(text, is_click=False)

    def input_clear(self):
        """
        input 组件清除文字(使用此函数之前必须确保输入框处于输入状态)
        :return:
        """
        self.at.e.edit_text().enter("", is_click=False)

    def textarea_text(self, text, index=0):
        self.at.e.edit_text().instance(index).enter(text, is_click=False)

    def textarea_clear(self, index=0):
        self.at.e.edit_text().instance(index).enter("", is_click=False)

    def map_select_location(self, name=None):
        if not name:
            # 不需要搜索地址
            if self.e.text("完成").enabled(True).exists(3):
                return self.e.text("完成").enabled(True).click_if_exists()
            else:  # 不能点完成，返回
                self.map_back_to_mp()
                return False
        can_search = True
        if (
            not self.at.e.text("搜索地点").click_if_exists()
            and not self.e.rid(
                "com.tencent.mm:id/send_loc_search_hint"
            ).click_if_exists()
        ):
            logger.error("当前客户端不支持搜索地点")
            can_search = False
        if not can_search:  # 同不需要搜索
            return self.map_select_location(None)
        self.at.e.edit_text().enter_chinese(name)
        self.at.adb.press_search()
        self.at.adb.press_back()
        while (
            self.at.e.cls_name(
                "android.widget.TextView").text_contains(name).exists()
        ):
            try:
                self.at.e.cls_name("android.widget.TextView").text_contains(
                    name
                ).click()
                if self.at.e.text("完成").exists:
                    break
            except Exception as e:
                logger.warning(str(e))
        self.at.e.text("完成").click()

    def map_back_to_mp(self):
        if not self.at.e.rid("com.tencent.mm:id/btn_back_txt").click_if_exists():
            self.e.cls_name("android.widget.TextView").text("取消").click()

    def deactivate(self, duration):
        self.at.adb.press_home()
        time.sleep(duration)
        self.at.adb.start_app("com.tencent.mm", "ui.LauncherUI", "-n")
        time.sleep(2)
        screen_width = int(self.at.device.width())
        screen_height = int(self.at.device.height())
        self.at.device.swipe(
            int(screen_width / 2),
            int(screen_height * 1 / 4),
            int(screen_width / 2),
            int(screen_height * 4 / 5),
            10,
        )
        time.sleep(2)
        self.textbounds = self.at.e.rid(
            "com.tencent.mm:id/test_mask").get_bounds()
        print(self.textbounds)
        xx = self.textbounds[0]
        yy = self.textbounds[1]
        self.at.adb.click_point(xx, yy)

    def allow_authorize(self, answer=True):
        # 点击按钮触发弹窗到客户端弹窗可能有一定延迟
        if answer:
            return self._handle_btn("允许", timeout=5.0)
        else:
            return self._handle_btn("拒绝", timeout=5.0)

    def allow_login(self, answer=True):
        self.allow_authorize(answer)

    def allow_get_user_info(self, answer=True):
        self.allow_authorize(answer)

    def allow_get_location(self, answer=True):
        self.allow_authorize(answer)

    def allow_get_we_run_data(self, answer=True):
        """
        处理获取微信运动数据确认弹框, 测试号可能需要开通微信运动
        :param answer: True or False
        :return:
        """
        if (
            self.e.cls_name("android.widget.TextView")
            .text("开启微信运动")
            .wait_exists(timeout=3.0)
        ):
            if not answer:
                self.at.adb.press_back()
                return False
            self.e.cls_name("android.widget.TextView").text("启用该功能").click()
        self.allow_authorize(answer)
        return True

    def allow_record(self, answer=True):
        self.allow_authorize(answer)

    def allow_write_photos_album(self, answer=True):
        """
        处理保存相册确认弹框
        :param answer: True or False
        :return:
        """
        self.allow_authorize(answer)

    def allow_camera(self, answer=True):
        """
        处理使用摄像头确认弹框
        :param answer: True or False
        :return:
        """
        self.allow_authorize(answer)

    def allow_get_user_phone(self, answer=True):
        """
        处理获取用户手机号码确认弹框
        :param answer: True or False
        :return:
        """
        self.allow_authorize(answer)

    def allow_send_subscribe_message(self, answer=True):
        """
        允许发送订阅消息
        """
        if answer:
            return self._handle_btn("", timeout=5.0, text_matches="允许|确定")
        else:
            return self._handle_btn("取消", timeout=5.0)

    def _handle_btn(self, btn_text="确定", timeout=0.5, text_matches=None):
        logger.debug(
            "handle android.widget.Button[%s]" % text_matches or btn_text)

        def do():
            e = self.e.cls_name("android.widget.Button").focusable(True)
            if text_matches:
                e.text_matches(text_matches)
            else:
                e.text(btn_text)
            return e.click_if_exists(timeout)

        try:
            ret = do()
        except (requests.ConnectionError, requests.ReadTimeout) as e:
            logger.error("handle btn error %s" % str(e))
            self.at.java_driver.reconnect()
            ret = do()
        except at.core.exceptions.UiNotFoundError:
            return False
        return ret

    def handle_modal(self, btn_text="确定", title=None, index=-1, force_title=False):
        if title:
            if not self.at.e.text_contains(title).exists():
                logger.info("没有出现预期弹窗：title[%s]", title)
                return False
        ret = self._handle_btn(btn_text)
        return ret

    def handle_action_sheet(self, item):
        ret = self.e.cls_name("android.widget.TextView").text(item).click()
        return ret

    def forward_miniprogram(self, name, text=None, create_new_chat=True):
        self.ui.action_menu.click()
        if not self.e.text("发送给朋友").click_if_exists():
            assert self.e.text("转发给朋友").click_if_exists(0.5), "找不到转发按钮"
        return self.forward_miniprogram_inside(name, text, create_new_chat)

    def _create_new_chat(self, timeout=0.5):
        # 点击"创建新聊天"
        return self.e.text_matches("创建新的?聊天").click_if_exists(timeout)

    def forward_miniprogram_inside(self, name, text=None, create_new_chat=True):
        if create_new_chat and self._create_new_chat():
            self.e.edit_text().enter(name)
            time.sleep(1)
            self.e.text_contains(name).click(True)
            if self.e.text("确定(1)").exists():
                self.e.text("确定(1)").enabled(True).click()
            else:
                self.e.text("完成(1)").enabled(True).click()
        else:
            self.e.text("搜索").click()
            time.sleep(1)
            self.e.edit_text().enter(name)
            time.sleep(1)
            self.e.text_contains(name).click(True)
            time.sleep(1)
        if text:
            self.e.edit_text().enter(text)
            self.at.adb.press_back()  # 键盘会挡住

        self.e.cls_name("android.widget.Button").text("发送").click()
        self.e.text("已转发").wait_disappear()

    def send_custom_message(self, message=None):
        pass

    def call_phone(self):
        pass

    def handle_picker(self, *items):
        instance = 0
        for item in items:
            input_elem = self.ui.comp_picker_input.instance(instance)
            next_elem = input_elem.parent().child("android.widget.Button")
            first_text = input_elem.get_text()
            while True:
                # todo: 要判断上滑还是下滑
                current_text = input_elem.get_text()
                if current_text == str(item):
                    break
                if first_text == str(item):
                    raise NativeError(" not found")
            instance += 1

    def get_authorize_settings(self):
        """
        在小程序的授权页面，获取小程序的授权设置
        :return:
        """
        ui_views = self.at.java_driver.dump_ui()
        setting_map = {}
        for ui_view in ui_views:
            if ui_view.cls_name == "android.view.View" and ui_view.content_desc in [
                "已开启",
                "已关闭",
            ]:
                check_status = True if ui_view.content_desc == "已开启" else False
                parant_view = ui_view.sibling().get_children()[0]
                setting_map[parant_view.text] = check_status
        return setting_map

    def back_from_authorize_setting(self):
        """
        从小程序授权页面跳转回小程序
        :return:
        """
        self.at.adb.press_back()

    def authorize_page_checkbox_enable(self, name, enable):
        """
        在小程序授权设置页面操作CheckBox
        :param name: 设置的名称
        :param enable: 是否打开
        :return:
        """
        setting_map = self.get_authorize_settings()
        if setting_map.get(name) == enable:
            return
        self.e.text(name).parent().instance(2).child().cls_name(
            "android.view.View"
        ).click()
        if not enable:
            self.e.cls_name("android.widget.Button").text(
                "关闭授权").click_if_exists(5)

    def release(self):
        logger.info("Native release")
        self.release_auto_authorize()
        if self.perf_flag:
            self.stop_get_perf()
        self.at.release()
        self._empty_base_screen_dir(self.outputs_screen)  # 清空截图目录

    def start_wechat(self):
        if self.at.adb.app_is_running(WECHAT_PACKAGE):
            self.at.adb.stop_app(WECHAT_PACKAGE)  # 先关掉
        self.at.adb.start_app(WECHAT_PACKAGE, WECHAT_ACTIVITY)

    def fold_keybroad(self):
        self.at.adb.press_back()

    def to_main_ui(self, timeout=3):
        el1 = self.e.pkg(WECHAT_PACKAGE).desc("返回")
        el2 = self.e.pkg(WECHAT_PACKAGE).desc("关闭")
        while True:
            try:
                if el1.exists(timeout):
                    el1.click()
                elif el2.exists(timeout):
                    el2.click()
                else:
                    break
            except:
                logger.exception("返回 failed")
                pass

    def stop_wechat(self):
        self.at.adb.stop_app(WECHAT_PACKAGE)

    def click_coordinate(self, x, y):
        self.at.adb.click_point(x, y)

    def click_point(self, x, y):
        """
        Alias for click_coordinate
        """
        return self.click_coordinate(x, y)

    def get_mem_used_new(self, pkg_name, pid):
        used = 0
        i = 0
        m = None
        m1 = None
        m2 = None
        cmd = "dumpsys meminfo %s" % pkg_name
        # logger.info(cmd)
        output_mem = self.at.adb.run_shell(cmd)
        # logger.info(output_mem)
        r = re.compile(r"TOTAL\s+(\d+)")

        r2 = re.compile(r"size:\s+\S+\s+\S+\s+\S+\s+(\d+)")
        ls = re.split(r"[\r\n]+", output_mem)
        # logger.info(ls)

        for line in ls:
            # i = i + 1
            # if i == 2:
            #     if line.find(pkg_name):
            #         logger.info("line is %s"%line)
            #         m1 = line.split("K")
            m = r.search(line)

            m2 = r2.search(line)

            m1 = line.find(pkg_name)
            # if m1:
            #     search_k = line.find("K:")
            #     search_pid = line.find("pid")
            #     if search_k and search_pid:
            #         num = line.split("K:")[0]
            #         logger.info("num is %s" % num)
            #         used = int(num) / 1024

            if m:
                used = int(m.group(1)) / 1024

            elif m2:
                used = int(m2.group(1)) / 1024

            # elif m1:
            #     logger.info("m1 is %s" % m1)
            #     used = int(m1) / 1024
        if used == 0:
            try:
                used = self.get_mem_used_new_doudi(output_mem, pkg_name, pid)
            except Exception as e:
                logger.error(e)
        return str(used)

    def get_mem_used_new_doudi(self, output_mem, processname, pid):
        used = 0
        if output_mem.find("Total PSS by process"):
            ls = re.split(r"[\r\n]+", output_mem)
            tag = processname + " (pid " + str(pid) + " / activities)"
            for line in ls:
                if line.find(tag) > -1:
                    used_str = line.split("K: ")[0]
                    used = int(used_str.replace(",", "")) / 1024
                    break
        return used

    def get_cpu_rate_by_file(
        self, mPid, mLastPidUserCpuTime, mLastPidKernelCpuTime, mLastTotalCpuTime
    ):
        # 计算cpu，读取/proc/stat的数据，计算cpuTime
        # 读取/proc/mPid/stat的数据，计算当前小程序的cpu数据
        pid_stat_file = "/proc/" + str(mPid) + "/stat"
        outputs = self.at.adb.run_shell("cat %s" % (pid_stat_file))
        # logger.info(outputs)
        pid_cpu_info_list = outputs.split(" ")
        # logger.info(pid_cpu_info_list)
        if len(pid_cpu_info_list) < 17:
            return 0, mLastPidUserCpuTime, mLastPidKernelCpuTime, mLastTotalCpuTime
        cpuTime = self.get_cpu_time()
        # logger.info(cpuTime)
        # 该进程处于用户态的时间
        pidUTime = int(pid_cpu_info_list[13])
        # logger.info(pidUTime)
        # 该进程处于内核态的时间
        pidSTime = int(pid_cpu_info_list[14])
        # logger.info(pidSTime)
        pidCpuUsage = 0
        # logger.info(mLastPidUserCpuTime)
        if mLastTotalCpuTime != 0:
            pidUserCpuUsage = (
                float(pidUTime - mLastPidUserCpuTime)
                / float(cpuTime - mLastTotalCpuTime)
            ) * 100
            pidKernelCpuUsage = (
                float(pidSTime - mLastPidKernelCpuTime)
                / float(cpuTime - mLastTotalCpuTime)
            ) * 100
            pidUserCpuUsage = max(0, pidUserCpuUsage)
            pidKernelCpuUsage = max(0, pidKernelCpuUsage)
            pidCpuUsage = pidUserCpuUsage + pidKernelCpuUsage

        mLastTotalCpuTime = cpuTime
        mLastPidUserCpuTime = pidUTime
        mLastPidKernelCpuTime = pidSTime
        # logger.info(pidCpuUsage)
        return (
            pidCpuUsage,
            mLastPidUserCpuTime,
            mLastPidKernelCpuTime,
            mLastTotalCpuTime,
        )

    def get_cpu_time(self):
        stat_file = "/proc/stat"
        outputs = self.at.adb.run_shell("cat %s" % (stat_file))
        # logger.info(outputs)
        lines = outputs.split("\n")
        list = lines[0].split(" ")
        # logger.info(list)
        if len(list) < 9:
            return 0
        user = int(list[2])
        nice = int(list[3])
        system = int(list[4])
        idle = int(list[5])
        ioWait = int(list[6])
        hardIrq = int(list[7])
        softIrq = int(list[8])
        stealTime = int(list[9])

        cpuTime = user + nice + system + idle + ioWait + hardIrq + softIrq + stealTime
        return cpuTime

    def write_perf_data(self, processname, pid, curview, timeinterval):
        # 对齐
        mLastPidUserCpuTime = 0
        mLastPidKernelCpuTime = 0
        mLastTotalCpuTime = 0
        while self.perf_flag:
            stime = time.time()
            # get cpu
            (
                perf_cpu,
                mLastPidUserCpuTime,
                mLastPidKernelCpuTime,
                mLastTotalCpuTime,
            ) = self.get_cpu_rate_by_file(
                pid, mLastPidUserCpuTime, mLastPidKernelCpuTime, mLastTotalCpuTime
            )
            # get fps
            if curview:
                fps_lines = self.at.adb.get_fps(curview)
                if len(fps_lines) <= 8:
                    doudi_currentview = (
                        "com.tencent.mm/com.tencent.mm.plugin.appbrand.ui.AppBrandUI#0"
                    )
                    fps_lines = self.at.adb.get_fps(doudi_currentview)
                try:
                    refresh_period, timestamps1 = self._collectFPSData(
                        fps_lines)
                    fps_data = self._CalculateResults(
                        refresh_period, timestamps1)
                except Exception as e:
                    logger.error(e)
                    # logger.info(fps_lines)
                    fps_data = 0

            else:
                fps_data = 0
            # get mem
            perf_mem = self.get_mem_used_new(processname, pid)

            # record
            logger.info(
                "perf_cpu: %s, fps_data: %s, perf_mem: %s"
                % (perf_cpu, fps_data, perf_mem)
            )
            timestamp = int(time.time())
            self.perf_data.append(
                {
                    "cpu": perf_cpu,
                    "mem": float(perf_mem),
                    "fps": fps_data,
                    "timestamp": timestamp,
                }
            )
            self._screen_shot("%d.png" % timestamp)
            etime = time.time()
            if etime - stime > timeinterval:
                continue
            time.sleep(etime - stime)

    def _start_get_perf(self, timeinterval=15):
        self.perf_flag = True
        retry = 3
        while retry > 0 and self.perf_flag:
            retry -= 1
            processname, pid = self.at.adb.get_current_active_process(
                re.escape("com.tencent.mm:appbrand") + "\d+")
            logger.info("processname [%s] pid [%s]" %
                        (str(processname), str(pid)))
            self.at.adb.clearbuffer()
            curview = self.at.adb.get_current_active_view(re.escape(
                "com.tencent.mm/com.tencent.mm.plugin.appbrand.ui.AppBrandUI") + "\d*#\d+")
            if (not processname) or (not curview):
                logger.error("current activity is not appbrand")
                time.sleep(2)
                continue
            else:
                break
        if processname and curview:
            try:
                self.perf_data = []
                self.write_perf_data(processname, pid, curview, timeinterval)
                return self.perf_flag
            except:
                self.perf_flag = False
                return self.perf_flag
        else:
            self.perf_flag = False
            return self.perf_flag

    def start_get_perf(self, timeinterval=15):
        if self.perf_flag:  # 一个线程就够了
            return True
        self.perf_thread = threading.Thread(
            target=self._start_get_perf,
            args=(timeinterval,),
        )
        self.perf_thread.daemon = True
        self.perf_thread.start()
        return True

    def stop_get_perf(self):
        self.perf_flag = False
        if self.perf_thread:
            self.perf_thread.join()
        if self.perf_data:
            perf_data_str = json.dumps(self.perf_data)
            self.perf_data = []
            return perf_data_str
        else:
            logger.error("get perf data fail")
            return ""

    def get_pay_value(self):
        try:
            if self.e.text_contains("￥").exists():
                return self.e.text_contains("￥").get_text()
            else:
                return ""
        except:
            return ""

    def _check_pay_modal_version(self):
        if not self.pay_modal_version:  # 先检测版本
            self._get_current_views()
            if self._el_exist_in_current_view(self.e.rid("com.tencent.mm:id/tenpay_keyboard_0")):
                self.pay_modal_version = 2
            elif self._el_exist_in_current_view(self.e.text_contains("请输入支付密码")) and self._el_exist_in_current_view(self.e.text_contains("￥")):
                self.pay_modal_version = 1
            else:
                raise TypeError("暂不支持当前微信客户端版本")
        return self.pay_modal_version

    def input_pay_password(self, psw=""):
        check_flag = self.e.text("请输入支付密码").click_if_exists(5)
        if not check_flag:
            return False
        if not psw:
            raise TypeError("未传入支付密码")
        psw = str(psw)
        if type(eval(psw)) is not int:
            raise TypeError("非法支付密码字符串")
        elif len(psw) != 6:
            raise TypeError("密码长度必须为6位数")
        self._check_pay_modal_version()
        for number in psw:
            if self.pay_modal_version == 1:
                point = self._get_number_point(number)
                self.at.device.click_on_point(point["x"], point["y"])
            elif self.pay_modal_version == 2:
                self.e.rid(f"com.tencent.mm:id/tenpay_keyboard_{number}").click()

        if self.e.text("支付成功").exists(10):
            self.e.text("完成").click(is_scroll=True)
        else:
            raise TypeError("支付失败")

    def close_payment_dialog(self):
        if self.e.text_contains("￥").exists(10):
            if not self.e.desc("关闭").click_if_exists():
                # 找不到关闭按钮试下直接返回
                self._press_back()
        else:
            if self.e.text_contains("支付方式").exists():
                self.at.adb.press_back()  # 有可能找不到输入框，先后退尝试
                return True
            logger.error("支付框不存在")
        return False

    def text_exists(self, text="", iscontain=False, wait_seconds=5):
        if iscontain:
            return self.e.text_contains(text=text).exists(wait_seconds)
        else:
            return self.e.text(text=text).exists(wait_seconds)

    def text_click(self, text="", iscontain=False):
        if iscontain:
            return self.e.text_contains(text=text).click(is_scroll=True)
        else:
            return self.e.text(text=text).click(is_scroll=True)

    def get_system_info(self):
        return self.at.adb.desc

    def _press_back(self):
        try:
            self.at.adb.press_key_code(at.keycode.KEYCODE_BACK)
        except:
            return False
        return True

    def is_app_in_foreground(self, appid):
        # exists text like appid:page_path:VISIBLE
        return self.e.text_contains(text=appid).exists(0.5)

    # back_to_miniprogram needed
    def _is_in_wechat(self, activity: str):
        return activity.startswith(WECHAT_PACKAGE)

    def _is_in_wechat_main(self, activity: str):
        return activity.endswith(WECHAT_ACTIVITY)

    def _is_in_miniprogram(self, activity: str):
        # return re.sub(r"\d+$", "", activity).endswith(MINIPROGRAM_ACTIVITY)
        temp = re.sub(r"\d+$", "", activity)
        return temp.endswith(MINIPROGRAM_ACTIVITY) or temp.endswith(
            MINIPROGRAM_PLUGIN_ACTIVITY
        )

    def _is_in_target_miniprogram(self, appid: str):
        if not appid:
            return True
        appids = []
        for i in self.at.java_driver.dump_ui():
            match = re.match("^(wx\w+):\w+$", i.content_desc)
            if match:
                appids.append(match.group(1))
        return appids[-1] == appid if len(appids) > 0 else False

    def _close_miniprogram(self):
        return self._press_back()

    def _get_any_modal(self, confirm=False):
        """
        confirm == True: 确认/允许
        confirm == False: 拒绝/取消
        蒙层下有button可以点击, 可以覆盖:
        1. 授权弹窗 —— 拒绝
        2. 分享弹窗 —— 取消/发送
        3. 模态弹窗 —— 取消/确定
        4. ACTION SHEET暂不支持
        """
        self._get_current_views()  # 刷新一下当前所有的views信息
        modals = []
        buttons = ["允许", "确认", "确定"] if confirm else ["拒绝", "取消"]
        for button in buttons:
            btn = (
                self.e.rid("android:id/content")
                .child()
                .focusable(True)
                .cls_name("android.widget.Button")
                .text(button)
            )
            if self._el_exist_in_current_view(btn):
                modals.append(btn)

        if not modals and not confirm:  # 兜底弹窗
            ok = (
                self.e.rid("android:id/content")
                .child()
                .focusable(True)
                .cls_name("android.widget.Button")
                .text("确定")
            )
            if self._el_exist_in_current_view(ok):
                modals.append(ok)

        return modals

    def _get_current_activity(self):
        output = self.at.adb.run_adb(
            [
                "shell",
                'dumpsys activity activities | grep -E "mFocusedActivity|mResumedActivity"',
            ]
        )
        logger.debug(output)
        for line in output.split("\n"):
            line = line.strip()
            m = re.search(r"((\w+?\.)+?(\w+)/(\.\w+)+)", line)
            if m:
                logger.info(f"current activity is {m.group(0)}")
                return m.group(0)
        return ""

    def _is_in_payment(self):
        return self.e.text_contains("￥").exists(0.5) or self.e.text_contains(
            "支付方式"
        ).exists(0.5)

    def _handle_modal(self, modals):
        if not modals:
            return ModalStatus.OK
        if isinstance(modals, (tuple, list)):
            success_modals = []
            ret = ModalStatus.OK
            for modal in modals:
                logger.info(f"handle modal: {modal}")
                try:
                    rid = modal.get_view().rid
                except at.core.exceptions.UiNotFoundError:
                    return ModalStatus.NotFound
                if modal.click_if_exists(0):
                    if not rid:
                        ret = ModalStatus.NotOfficialModal
                    success_modals.append(modal)
            logger.info(
                f"need handle {len(modals)} modal, success {len(success_modals)}"
            )
            if len(success_modals) > 0:
                return ret
        else:
            modal = modals
            logger.info(f"handle modal: {modal}")
            try:
                rid = modal.get_view().rid
            except at.core.exceptions.UiNotFoundError:
                return ModalStatus.NotFound
            if modal.click_if_exists(0):
                if not rid:
                    return ModalStatus.NotOfficialModal
                return ModalStatus.OK
            return ModalStatus.Error
        return ModalStatus.Error

    def _get_number_point(self, number):
        """
        获取数字的中心坐标
        :param number:
        :return:
        """
        if type(number) is str:
            if type(eval(number)) is not int:
                raise TypeError("number应该为int")
            number = int(number)
        rect = self.e.rid("com.tencent.mm:id/g60").get_rect()
        column_distance = (rect.right - rect.left) / 3  # 列距
        line_distance = (rect.bottom - rect.top) / 4  # 行距

        start_center_point = {
            "x": rect.left + column_distance / 2,
            "y": rect.top + line_distance / 2,
        }

        if number == 1:
            x = start_center_point["x"]
            y = start_center_point["y"]
        elif number == 0:
            x = start_center_point["x"] + column_distance
            y = start_center_point["y"] + line_distance * 3
        else:
            row_num = (number - 1) // 3  # 跟起点相差几行
            column_num = number % 3
            if column_num == 0:
                column_num = 3
            column_num = column_num - 1  # 跟起点相差几列
            x = start_center_point["x"] + column_distance * column_num
            y = start_center_point["y"] + line_distance * row_num
        print("number:{0} ===> Point({1},{2})".format(number, x, y))
        return {"x": x, "y": y}

    def _collectFPSData(self, results):
        timestamps = []
        if len(results) < 128:
            return (0, timestamps)
        nanoseconds_per_second = 1e9
        refresh_period = int(results[0]) / nanoseconds_per_second
        # logger.debug("refresh_period: %s" % refresh_period)
        pending_fence_timestamp = (1 << 63) - 1
        for line in results[1:]:
            fields = line.split()
            if len(fields) != 3:
                continue
            if not fields[0].isnumeric():
                continue
            if int(fields[0]) == 0:
                continue
            timestamp = int(fields[1])
            if timestamp == pending_fence_timestamp:
                continue
            timestamp /= nanoseconds_per_second
            timestamps.append(timestamp)
        # logger.error("timestamps: %s" % timestamps)
        return (refresh_period, timestamps)

    def _GetNormalizedDeltas(self, data, refresh_period, min_normalized_delta=None):
        deltas = [t2 - t1 for t1, t2 in zip(data, data[1:])]
        if min_normalized_delta is not None:
            deltas = filter(
                lambda d: d / refresh_period >= min_normalized_delta, deltas
            )
            deltas = list(deltas)
        return (deltas, [delta / refresh_period for delta in deltas])

    def _CalculateResults(self, refresh_period, timestamps):
        """Returns a list of SurfaceStatsCollector.Result."""
        frame_count = len(timestamps)
        if frame_count == 0:
            return 0
        seconds = timestamps[-1] - timestamps[0]
        frame_lengths, normalized_frame_lengths = self._GetNormalizedDeltas(
            timestamps, refresh_period, _MIN_NORMALIZED_FRAME_LENGTH
        )
        if len(frame_lengths) < frame_count - 1:
            logging.warning("Skipping frame lengths that are too short.")
            frame_count = len(frame_lengths) + 1
        if len(frame_lengths) == 0:
            # raise Exception("No valid frames lengths found.")
            return 0
        return int(round((frame_count - 1) / seconds))

    @property
    def e(self):
        return self.at.e

    def _screen_shot(self, filename):
        return self.screen_shot(os.path.join(self.outputs_screen, filename))

    # 云环境上莫名其妙卡死在这里了。。。
    @wait(60, False)
    def check_connection(self, *args):
        # 检查atsub链接
        if self.at.java_driver.ping():
            return True
        # reconnect
        try:
            self.at.java_driver.close_remote()
            time.sleep(1)
            self.at.java_driver._init(True)
        except Exception as e:
            logger.exception(e)
            return False
        return self.at.java_driver.is_remote_running()


if __name__ == "__main__":
    n = WXAndroidNative({"lang": "en"})
    n.handle_modal("queding", "")
