#!/usr/bin/env python3
# Created by xiazeng on 2019-05-22

import logging
import time
import os
import shutil
import json
import threading
import types
from functools import wraps

from minium.utils.utils import timeout
from ..exception import *
from ...utils.emitter import ee

logger = logging.getLogger("minium")


def call_funtion_log(func, name: str):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"call {name}")
        result = func(*args, **kwargs)
        if name.find(".handle") > 0 or name.find(".allow") > 0:
            logger.info(f"{name} return {str(result)}")
        logger.info(f"call {name} end")
        return result

    return wrapper


class NativeMetaClass(type):
    def __new__(mcs, cls_name, bases, attr_dict):
        for k, v in attr_dict.items():
            if isinstance(v, types.FunctionType) and not k.startswith("_"):
                attr_dict[k] = call_funtion_log(v, f"{cls_name}.{k}")
        return type.__new__(mcs, cls_name, bases, attr_dict)


class BaseNative(object, metaclass=NativeMetaClass):
    def __init__(self, json_conf):
        self.json_conf = json_conf
        self.perf_data = []
        self.__auto_authorize_thread = None
        self.__auto_authorize_lock = threading.Condition()
        self.__auto_authorize_flag = False
        self.__last_notify_time = time.time()
        self.auto_authorize = False  # 是否自动授权

    def release(self):
        self.release_auto_authorize()

    def start_wechat(self):
        """
        启动微信
        :return:
        """
        raise NotImplementedError()

    def stop_wechat(self):
        """
        启动微信
        :return:
        """
        raise NotImplementedError()

    def connect_weapp(self, path):
        """
        扫码图片
        :param path:图片名称
        :return:
        """
        raise NotImplementedError()

    def screen_shot(self, filename, return_format="raw"):
        """
        截图
        :param filename: 文件存放的路径
        :param return_format: 除了将截图保存在本地之外, 需要返回的图片内容格式: raw(default) or pillow
        :return: raw data or PIL.Image
        """
        raise NotImplementedError()

    def pick_media_file(
        self,
        cap_type="camera",
        media_type="photo",
        original=False,
        duration=5.0,
        names=None,
    ):
        """
        获取媒体文件
        :param cap_type: camera: 拍摄 | album: 从相册获取
        :param names: 传入一个 list 选择多张照片或者视频(照片和视频不能同时选择, 且图片最多 9 张, 视频一次只能选择一个)
        :param media_type: photo 或者 video
        :param duration: 拍摄时长
        :param original: 是否选择原图(仅图片)
        :return:
        """
        raise NotImplementedError()

    def input_text(self, text):
        """
        input 组件填写文字
        :param text: 内容
        :return:
        """
        raise NotImplementedError()

    def input_clear(self):
        """
        input 组件清除文字(使用此函数之前必须确保输入框处于输入状态)
        :return:
        """
        raise NotImplementedError()

    def textarea_text(self, text, index=1):
        """
        给 textarea 输入文字需要在小程序层提供该 textarea 的 index 信息
        :param text: 内容
        :param index: 多个 textarea 同时存在一个页面从上往下排序, 计数从 1 开始
        :return:
        """
        raise NotImplementedError()

    def textarea_clear(self, index=0):
        """
        给 textarea 清除文字需要在小程序层提供该 textarea 的 index 信息
        :param index: 多个 textarea 同时存在一个页面从上往下排序, 计数从 1 开始
        :return:
        """
        raise NotImplementedError()

    def allow_authorize(self, answer=True, title=None):
        """
        处理授权确认弹框
        :param answer: True or False
        :return: bool
        """
        raise NotImplementedError()

    def allow_login(self, answer=True):
        """
        处理微信登陆确认弹框
        :param answer: True or False
        :return:
        """
        raise NotImplementedError()

    def allow_get_user_info(self, answer=True):
        """
        处理获取用户信息确认弹框
        :param answer: True or False
        :return:
        """
        raise NotImplementedError()

    def allow_get_location(self, answer=True):
        """
        处理获取位置信息确认弹框
        :param answer: True or False
        :return:
        """
        raise NotImplementedError()

    def allow_get_we_run_data(self, answer=True):
        """
        处理获取微信运动数据确认弹框
        :param answer: True or False
        :return:
        """
        raise NotImplementedError()

    def allow_record(self, answer=True):
        """
        处理获取录音权限确认弹框
        :param answer: True or False
        :return:
        """
        raise NotImplementedError()

    def allow_write_photos_album(self, answer=True):
        """
        处理保存相册确认弹框
        :param answer: True or False
        :return:
        """
        raise NotImplementedError()

    def allow_camera(self, answer=True):
        """
        处理使用摄像头确认弹框
        :param answer: True or False
        :return:
        """
        raise NotImplementedError()

    def allow_get_user_phone(self, answer=True):
        """
        处理获取用户手机号码确认弹框
        :param answer: True or False
        :return:
        """
        raise NotImplementedError()

    def allow_send_subscribe_message(self, answer=True):
        """
        允许发送订阅消息
        """
        raise NotImplementedError()

    def handle_modal(self, btn_text="确定", title=None, index=-1, force_title=False):
        """
        处理模态弹窗
        :param title: 传入弹窗的 title 可以校验当前弹窗是否为预期弹窗
        :param btn_text: 根据传入的 name 进行点击
        :return:
        """
        raise NotImplementedError()

    def handle_action_sheet(self, item):
        """
        处理上拉菜单
        :param item: 要选择的 item
        :return:
        """
        raise NotImplementedError()

    def forward_miniprogram(
        self, name: str, text: str = None, create_new_chat: bool = True
    ):
        """
        通过右上角更多菜单转发小程序
        :type text: 分享携带的内容
        :param names: 要分享的人
        :param create_new_chat: 是否创建群聊
        :return:
        """
        raise NotImplementedError()

    def forward_miniprogram_inside(
        self, name: str, text: str = None, create_new_chat: bool = True
    ):
        """
        小程序内触发转发小程序
        :param names: 要分享的人
        :param create_new_chat: 是否创建群聊
        :return:
        """
        raise NotImplementedError()

    def send_custom_message(self, message=None):
        """
        处理小程序im 发送自定义消息
        :param message: 消息内容
        :return:
        """
        raise NotImplementedError()

    def phone_call(self):
        """
        处理小程序拨打电话
        :return:
        """
        raise NotImplementedError()

    def map_select_location(self, name=None):
        """
        原生地图组件选择位置
        :param name: 位置名称
        :return:
        """
        raise NotImplementedError()

    def map_back_to_mp(self):
        """
        原生地图组件查看定位,返回小程序
        :return:
        """
        raise NotImplementedError()

    def deactivate(self, duration):
        """
        使微信进入后台一段时间, 再切回前台
        :param duration: float
        :return: NULL
        """
        raise NotImplementedError()

    def get_authorize_settings(self):
        """
        在小程序的授权页面，获取小程序的授权设置
        :return:
        """
        raise NotImplementedError()

    def back_from_authorize_setting(self):
        """
        从小程序授权页面跳转回小程序
        :return:
        """
        raise NotImplementedError()

    def authorize_page_checkbox_enable(self, name, enable):
        """
        在小程序授权设置页面操作CheckBox
        :param name: 设置的名称
        :param enable: 是否打开
        :return:
        """
        raise NotImplementedError()

    def start_get_perf(self, timeinterval=15):
        """
        开始获取性能数据
        :param timeinterval: 抽样时间间隔
        :return: boolen
        """
        return False

    def stop_get_perf(self):
        """
        停止获取性能数据
        :return: string: json.dumps([{cpu, mem, fps, timestamp}])
        """
        pass

    def get_perf_data(
        self, start_timestamp: int = None, end_timestamp: int = None
    ) -> str:
        """
        获取[start_timestamp, end_timestamp]区间内的perf data
        :start_timestamp: 开始时间戳，如果为none，不过滤开始时间，start_timestamp后没有任何数据且perf data列表有数据，返回最后一个数据(理解为数据没有变化)
        :end_timestamp: 结束时间戳，如果为none，不过滤结束时间, 如果end_timestamp比第一个元素时间还小，返回空
        :return: "[{timestamp, cpu, mem, fps}]" or ""
        """
        if not self.perf_data:
            return ""
        if start_timestamp is None and end_timestamp is None:
            return json.dumps(self.perf_data)
        end_index = len(self.perf_data)  # 如果之后还有数据入列表也忽略，数据从后往前搜索
        if end_timestamp is not None:  # search end_index
            while self.perf_data[end_index - 1]["timestamp"] > end_timestamp:
                end_index -= 1
                if end_index == 0:
                    break
        if end_index == 0:
            return ""
        if start_timestamp is None or end_index == 1:
            return json.dumps(self.perf_data[:end_index])
        else:  # search start_index
            start_index = end_index - 1  # at least equal 1
            while self.perf_data[start_index - 1]["timestamp"] >= start_timestamp:
                start_index -= 1
                if start_index == 0:
                    break
            return json.dumps(self.perf_data[start_index:end_index])

    def get_start_up(self):
        """
        获取小程序启动时间
        """
        return 0

    def start_get_start_up(self):
        """
        开始监听启动时间
        """
        pass

    def stop_get_start_up(self):
        """
        结束监听启动时间
        :return: number
        """
        return 0

    def click_coordinate(self, x, y):
        """
        按坐标点击
        :param x:
        :param y:
        :return:
        """
        raise NotImplementedError()

    def get_pay_value(self):
        """
        获取支付金额
        """
        raise NotImplementedError()

    def input_pay_password(self):
        """
        输入支付密码
        """
        raise NotImplementedError()

    def close_payment_dialog(self):
        """
        关闭支付弹窗
        """
        raise NotImplementedError()

    def text_exists(self, text="", iscontain=False, wait_seconds=5):
        """
        检测是否存在text
        """
        raise NotImplementedError()

    def text_click(self, text="", iscontain=False):
        """
        点击内容为text的控件
        """
        raise NotImplementedError()

    def hide_keyboard(self):
        """
        隐藏键盘
        :return:
        """
        raise NotImplementedError()

    def is_app_in_foreground(self, appid):
        """
        判断{appid}的小程序是否在前台，默认不会退后台
        :return: bool
        """
        return True

    def check_connection(self, *args):
        """
        检查真机调试通道是否还存在, 如果断连则重连
        :return: bool
        """
        return True

    def _get_current_activity(self):
        return ""

    def _is_in_wechat(self, activity: str):
        return True

    def _is_in_wechat_main(self, activity: str):
        return False

    def _is_in_miniprogram(self, activity: str):
        """
        需要甄别: 插件页面、webview页面、普通页面
        """
        return True

    def _is_in_target_miniprogram(self, appid: str):
        return True

    def _close_miniprogram(self):
        return True

    def _get_any_modal(self, confirm=False):
        return None

    def _is_in_payment(self):
        return False

    def _handle_modal(self, modal):
        if not modal:
            return ModalStatus.OK
        logger.info(f"handle modal: {modal}")
        if modal.click_if_exists(0.5):
            return ModalStatus.OK
        return ModalStatus.Error

    def _back_to_target_miniprogram(self, appid):
        if not self._is_in_target_miniprogram(appid):
            logger.error(f"not in {appid}")
            # 先判断是不是目标小程序, 尝试3次
            for i in range(1, 4):
                logger.error(f"try to close miniprogram {i} times")
                if not self._close_miniprogram():  # 无法操作关闭小程序
                    logger.error("close miniprogram error, relaunch")
                    return ResetError.RELAUNCH_APP
                time.sleep(1)
                if self._is_in_target_miniprogram(appid):
                    logger.info(f"now in {appid}")
                    break
                if i == 3:  # 3次仍未回到目标小程序
                    logger.error(f"try to close miniprogram {i} times but still error, relaunch")
                    return ResetError.RELAUNCH_APP
        has_any_modal = self._get_any_modal(self.allow_authorize)  # 获取目标小程序中的modal
        # 已经回到当前小程序
        if not has_any_modal:
            return ResetError.OK
        return has_any_modal

    def _handle_any_modal(self, has_any_modal, cnt, crash_cnt):
        ret = None
        while has_any_modal:  # 有弹窗, 点击直到没有
            ret = self._handle_modal(has_any_modal)
            if ret == ModalStatus.OK:
                cnt = 3
                crash_cnt -= 1  # 虽然点击指令执行成功了，但很多情况是没有点击到的
                time.sleep(1)
            elif ret == ModalStatus.NotOfficialModal:
                # 操作成功了，但弹窗可能并不是官方提供的弹窗
                cnt -= 1
                crash_cnt -= 1  # 虽然点击指令执行成功了，但很多情况时没有点击到的
                time.sleep(1)
            elif ret == ModalStatus.NotFound:
                break
            has_any_modal = self._get_any_modal(self.allow_authorize)
            if ret == ModalStatus.Error:
                break
            if crash_cnt < 0:
                break
        return ret, has_any_modal, cnt, crash_cnt

    def back_to_miniprogram(self, appid=""):
        """
        返回小程序
        :return: ResetError, 0: 返回成功. -1: 无法识别的错误. -2: 需要重新加载小程序. -3: 需要重新加载微信
        """
        crash_cnt = 15  # 防止预期之外的死循环, 每一次操作都会计数减一
        cnt = 3  # 防止一直检测循环, 当有检测操作成功的，重置为初始次数
        last_activity = None
        while cnt > 0:
            logger.info(f"try back_to_miniprogram {cnt}")
            cnt -= 1
            # 检测是否还在微信
            current_activity = self._get_current_activity()
            if not self._is_in_wechat(current_activity):
                logger.error("current activity is %s, not wechat" % current_activity)
                return ResetError.RELAUNCH_APP
            # 已经回到了微信主程序
            if self._is_in_wechat_main(current_activity):
                logger.error(
                    "already back to wechat main activity, please relaunch miniprogram"
                )
                return ResetError.RELAUNCH_MINIPROGRAM

            has_any_modal = None
            # 回到目标小程序
            if self._is_in_miniprogram(current_activity):
                ret = self._back_to_target_miniprogram(appid)
                if isinstance(ret, ResetError):
                    return ret
                has_any_modal = ret
            else:
                logger.error("not in miniprogram")
                has_any_modal = self._get_any_modal(self.allow_authorize)  # 不在小程序中也需要尝试检查一下弹窗
            # 看看是不是支付的弹窗
            if self._is_in_payment():
                logger.warning("有支付弹窗")
                if self.close_payment_dialog():
                    logger.info("成功关闭支付弹窗")
                    cnt = 3
                    crash_cnt -= 1
                continue
            # 无论是否在小程序进程，都可能遗留弹窗，如果检测到有，则点击"取消/拒绝"
            ret, has_any_modal, cnt, crash_cnt = self._handle_any_modal(
                has_any_modal, cnt, crash_cnt
            )
            logger.info(f"finish handle modals {ret}")
            if ret is not None:
                current_activity = (
                    self._get_current_activity()
                )  # 操作完可能对当前activity有所影响，应更新
            if not has_any_modal and self._is_in_miniprogram(current_activity):
                logger.info(f"back to miniprogram ok, current activity: {current_activity}")
                return ResetError.OK
            if (
                last_activity and last_activity != current_activity
            ):  # activity有变化了，认为操作有效可以reset循环
                cnt = 3
            last_activity = current_activity
            # 返回
            if not self._is_in_miniprogram(current_activity):
                self._press_back()
                crash_cnt -= 1
                time.sleep(1)
            if crash_cnt < 0:
                break
        logger.error(f"back to miniprogram error, current activity: {self._get_current_activity()}")
        return ResetError.ERROR

    def _press_back(self):
        """
        返回
        :return: bool
        """
        return True

    # @ee.on('notify')  # 不能直接修饰成员函数
    def notify(self):
        """
        通知auto authorize线程处理弹窗. 通知时机包括:
        1. tap/long_press/click之后
        2. after hook auth method
        """
        if not self.__auto_authorize_thread:
            return
        logger.debug("receive a notify signal")
        self.__notify()

    def set_auto_authorize(self, answer=True):
        """
        自动操作授权，操作时机等待 notify
        :params answer: True: 自动同意, False: 自动拒绝
        :return: bool
        """
        self.auto_authorize = answer
        if self.__auto_authorize_thread:
            return True
        self.__auto_authorize_thread = threading.Thread(
            target=self.__op_auto_authorize, args=(answer,)
        )
        self.__auto_authorize_thread.setDaemon(True)
        self.__auto_authorize_thread.start()
        ee.on("notify", self.notify)  # 监听相应函数
        return True

    def release_auto_authorize(self):
        """
        release auto authorize thread
        """
        if self.__auto_authorize_thread:
            # 移除监听事件
            ee.remove_all_listeners("notify")
            self.__auto_authorize_flag = False
            self.__notify()
            logger.info("stopping auto authorize thread")
            self.__auto_authorize_thread.join()
            logger.info("stop auto authorize thread")
            self.__auto_authorize_thread = None

    # protect method
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
        while time.time() - s < timeout:
            if func():
                return True
            time.sleep(interval)
        return False

    def _auto_authorize_callback(self, answer=True):
        """
        处理authorize的逻辑, 可重载
        """
        ret = True
        cnt = 10  # 最大处理10个授权窗口，防止死循环(检测到有元素 & 可以click，但实际点不动)
        while ret and cnt > 0:
            cnt -= 1
            try:
                ret = self.allow_authorize(answer)
            except NotImplementedError:
                #  未实现的处理方法，直接break进程
                return False
            time.sleep(1)
        return cnt > 0

    def _empty_base_screen_dir(self, dirname):
        if os.path.exists(dirname):
            if os.path.isdir(dirname):
                shutil.rmtree(dirname)
                time.sleep(1)
            else:
                os.remove(dirname)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    def __notify(self):
        self.__auto_authorize_lock.acquire()
        self.__auto_authorize_lock.notify_all()
        self.__last_notify_time = time.time() + 6  # 收到通知后6秒内还应该继续检测, 一般弹窗有滞后性
        self.__auto_authorize_lock.release()

    def __op_auto_authorize(self, answer):
        self.__auto_authorize_flag = True
        while self.__auto_authorize_flag:
            self.__auto_authorize_lock.acquire()
            ret = self.__auto_authorize_lock.wait(timeout=5)
            self.__auto_authorize_lock.release()
            if not ret and self.__last_notify_time < time.time():
                continue
            if not self.__auto_authorize_flag:
                break
            logger.debug("before auto_authorize_callback")
            ret = self._auto_authorize_callback(answer)
            logger.debug(
                "after auto_authorize_callback, %s. flag: %s"
                % (ret, self.__auto_authorize_flag)
            )
            if not ret:
                break


class NativeError(RuntimeError):
    pass
