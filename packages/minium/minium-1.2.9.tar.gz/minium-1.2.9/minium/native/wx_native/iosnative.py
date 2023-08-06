#!/usr/bin/env python3
# Created by xiazeng on 2019-05-22
import json
import logging
import threading
import platform
from .basenative import BaseNative
from ..lib.wx_wda import *

tidevice = None
OTHER_PACKAGE = "com.others.app"
WECHAT_PACKAGE = "com.tencent.xin"
WECHAT_ACTIVITY = "MainFrameViewController"
MINIPROGRAM_ACTIVITY = "WAWebViewController"
OTHER_ACTIVITY = "OtherActivity"

logger = logging.getLogger("minium")
if "Windows" in platform.platform():
    isWindows = True
else:
    isWindows = False


class WXIOSNative(BaseNative):
    useTIDevice = False

    def __init__(self, json_conf: dict):
        if json_conf is None:
            json_conf = {}
        super(WXIOSNative, self).__init__(json_conf)
        # 目标设备, 目标app
        self.udid = json_conf.get("device_info", {}).get("udid")
        self.bundle_id = json_conf.get("device_info", {}).get(
            "bundle_id", WECHAT_PACKAGE
        )
        # 使用xcode + wda project需要以下信息
        self.wda_project_path = json_conf.get("wda_project_path")
        self.wda_runner = None
        # 使用tidevice
        self.wda_bundle = json_conf.get("wda_bundle", None)
        # 目标app实例
        self.app = None
        # 获取性能的实例
        self.perf_flag = False
        self.perf = None
        self.perf_data = []
        self.last_cpu = 0
        self.last_fps = 0
        self.last_mem = 0
        # 健康弹窗处理
        self.health_modal_handle_thread = None
        self.stop_check = True
        self.check_done = True
        # screen_shot
        self.outputs_screen = os.path.join(
            json_conf.get("outputs") or os.path.dirname(os.path.realpath(__file__)),
            "image",
        )
        self._empty_base_screen_dir(self.outputs_screen)

    ###############################
    #                    interface                        #
    ###############################
    def start_wechat(self):
        """
        启动微信
        :return:
        """
        if self.wda_project_path and not isWindows:
            self.wda_runner = WebDriverRunner(self.udid, self.wda_project_path)
        else:
            self.wda_runner = TIDevice(self.udid, self.wda_bundle)
            self.useTIDevice = True
        for i in range(3):
            try:
                logger.info("第 %d 次启动微信, 共3次机会" % (i + 1))
                self.app = WdaUI(
                    server_url="http://localhost:%s" % self.wda_runner.port,
                    bundle_id=self.bundle_id,
                )
                self.app.session.set_alert_callback(self._alert_callback) if callable(
                    self._alert_callback
                ) else logger.error("Alert callback would not callable")
                logger.info("微信启动成功")
                # 重启多次可能会进入安全模式
                if self.app.session(
                    class_name="NavigationBar", text="安全模式"
                ).wait_exists(timeout=5.0):
                    while self.app.session(
                        class_name="Button", text="下一步"
                    ).click_if_exists(timeout=3.0):
                        time.sleep(1)
                    self.app.session(class_name="Button", text="进入微信").click_if_exists(
                        timeout=3.0
                    )
                return
            except Exception as e:
                if i == 2:
                    # e.args += "setup error: 第 %d 次启动微信失败" % (i + 1)
                    raise
                logger.error("setup error: 第 %d 次启动微信失败: %s" % ((i + 1), str(e)))
                if "Connection refused" in str(e):
                    logger.warning(
                        "Connection refused, 端口[%s]不可用，重新选择 iproxy 端口"
                        % self.wda_runner.port
                    )
                    self.wda_runner.remove_iproxy()
                    port = self.wda_runner.pick_unuse_port()
                    self.wda_runner.listen_port(port)
                    continue
                logger.info("正在重启 WebDriverAgent ...")
                self.wda_runner.start_driver()

    def connect_weapp(self, path):
        """
        有push的方式, 理应可以废掉
        """
        raise NotImplementedError("ios不再支持长按识别二维码的方式，请使用推送方式调用")
        filename = "remote_debug.jpg"
        r = requests.post(
            "https://stream.weixin.qq.com/weapp/UploadFile",
            files={filename: (filename, open(path, "rb"))},
        )
        if r.status_code != 200:
            logger.error(r.text)
            r.raise_for_status()

        url = "https://stream.weixin.qq.com/weapp/GetQRCodePage?file_name={0}".format(
            filename
        )
        self.app.session(class_name="Button", text="通讯录").click(timeout=10.0)
        self.app.session(class_name="SearchField", text="搜索").set_text("文件传输助手")
        self.app.session(xpath="//Table[1]/Cell[2]/Button[1]").click(timeout=10)
        self.app.session(class_name="TextView").set_text(url + "\n")
        self.app.session(class_name="Other", partial_text=url)[-1].click(timeout=10.0)
        self.app.session(class_name="WebView").subelems(
            class_name="Other", text="小程序web view测试"
        ).subelems(class_name="Image").tap_hold(3.0)
        self.app.session(partial_text="识别图中二维码").click(timeout=10.0)

    def screen_shot(self, filename: str, return_format: str = "raw") -> object:
        """
        截图
        :param filename: 文件存放的路径
        :param return_format: 除了将截图保存在本地之外, 需要返回的图片内容格式: raw(default) or pillow
        :return: raw data or PIL.Image
        """
        try:
            self.app.client.screenshot(png_filename=filename)
            return filename
        except Exception as e:

            logger.warning("screen shot failed, %s" % e)

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
        if cap_type == "album" and names is None:
            raise Exception("从相册选择照片必须提供照片名称, 可以通过 wda inspector 查看照片名称")
        if cap_type == "camera":
            self._capture_photo(media_type=media_type, duration=duration)
        elif cap_type == "album":
            if media_type == "photo":
                if isinstance(names, str):
                    names = [names]
                self._select_photos_from_album(names=names, original=original)
            elif media_type == "video":
                if isinstance(names, list):
                    names = names[0]
                self._select_video_from_album(name=names)

    def input_text(self, text):
        """
        input 组件填写文字(使用此函数之前必须确保输入框处于输入状态)
        :param text: 内容
        :return:
        """
        self.app.session(class_name="TextField").set_text(text)

    def input_clear(self):
        """
        input 组件清除文字(使用此函数之前必须确保输入框处于输入状态)
        :return:
        """
        self.app.session(class_name="TextField").clear_text()

    def textarea_text(self, text: str, index=0):
        """
        给 textarea 输入文字需要在小程序层提供该 textarea 的 index 信息
        :param text: 内容
        :param index: 多个 textarea 同时存在一个页面从上往下排序, 计数从 1 开始
        :return:
        """
        self.app.session(class_name="TextView")[index].set_text(text)

    def textarea_clear(self, index=0):
        """
        给 textarea 清除文字需要在小程序层提供该 textarea 的 index 信息
        :param index: 多个 textarea 同时存在一个页面从上往下排序, 计数从 1 开始
        :return:
        """
        self.app.session(class_name="TextView")[index].clear_text()

    def allow_authorize(self, answer=True, title=None):
        """
        处理授权确认弹框
        :param answer: True or False
        :return:
        """
        logger.debug("handle Button[%s], title[%s]" % ("允许" if answer else "拒绝", title))
        if title:
            return self.app.session(
                xpath='//*[contains(@label, "{title}")]/../../..//Button[@name="{text}"]'.format(
                    title=title, text="允许" if answer else "拒绝"
                )
            ).click_if_exists(timeout=10.0)
        else:
            return self.app.session(
                xpath='//Button[@label="授权说明"]/../../..//Button[@name="{text}"]'.format(
                    text="允许" if answer else "拒绝"
                )
            ).click_if_exists(timeout=10.0)

    def allow_login(self, answer=True):
        """
        处理微信登陆确认弹框
        :return:
        """
        if answer:
            self.app.session(class_name="Button", text="允许").click_if_exists(
                timeout=10.0
            )
        else:
            self.app.session(class_name="Button", text="拒绝").click_if_exists(
                timeout=10.0
            )

    def allow_get_user_info(self, answer=True):
        """
        处理获取用户信息确认弹框
        :param answer: True or False
        :return:
        """
        self.allow_authorize(answer, "获取你的昵称")

    def allow_get_location(self, answer=True):
        """
        处理获取位置信息确认弹框
        :param answer: True or False
        :return:
        """
        self.allow_authorize(answer, "获取你的位置信息")

    def allow_get_we_run_data(self, answer=True):
        """
        处理获取微信运动数据确认弹框
        :param answer: True: 允许 or False: 拒绝
        :return:

        备注：
        - 未启用微信运动时，启用微信运动后就立即授权使用了，无须再次授权允许
        - 开启微信运动后，ios可能会有健康弹窗，出现时间不定
        处理策略：
        1. 未开启微信运动，且授权操作为“否”(answer==False)：不开启微信运动，返回false
        2. 未开启微信运动，且授权操作为“是”(answer==True)：开启微信运动，监测健康弹窗
        3. 已经开启过微信运动：监测健康弹窗，允许微信获取健康数据，再在小程序授权弹窗中再处理对app的授权与否
        4. 如果曾经不允许微信获取健康数据，调用getWeRunData时，会弹modal窗"暂不能获取完整健康数据"，即使从系统拿不到,但数据还是能从后台拿, 如果有授权弹窗，返回{answer}，否则默认True
        5. 无授权弹窗出现，默认同意，返回True
        """
        # 开启微信运动后，直接就默认了授权使用微信运动了
        if self.app.session(class_name="NavigationBar", text="开启微信运动").wait_exists(
            timeout=3.0
        ):
            if not answer:
                self.app.session(text="关闭").click_if_exists(timeout=10)
                return False
            self.app.session(class_name="Button", text="启用该功能").click_if_exists(
                timeout=10
            )
        # 监测 "暂不能获取完整健康数据" 弹窗, 如果存在，则系统层面已经不允许获取健康数据，返回False
        if self.modal_exists("暂不能获取完整健康数据"):
            logger.error("暂不能获取完整健康数据")
            self.handle_modal("确定", title="暂不能获取完整健康数据")
            # 此时授权弹窗可能已经弹了出来, 即使从系统拿不到,但数据还是能从后台拿
            ret = self.allow_authorize(answer, "获取你的微信运动步数")
            return answer if ret else True
        # 开启之后ios可能会有健康弹窗，出现时间不定
        self.health_page_exists = False
        if not self.health_modal_handle_thread:

            def handle_health_modal():
                # print("handle_health_modal 1 %f" % time.time())
                while self.app.session.alert.exists:
                    self.app.session.alert.accept()
                    time.sleep(1)
                # print("handle_health_modal 2 %f" % time.time())
                if not self.app.search_text("想要访问并更新以下类别中的健康数据"):
                    print("handle_health_modal 3 %f" % time.time())
                    return False
                # print("health_page_exists wait %f" % time.time())
                self.health_page_exists = True
                switch = self.app.session(class_name="Switch", index=-1)
                if not self._wait(lambda: switch.exists, 10):
                    logger.error("Switch not exists")
                    return False
                if str(switch.value) == "0":
                    switch.click(timeout=5)
                accept = self.app.session(class_name="Button", text="允许", index=-1)
                if not self._wait(lambda: accept.exists and accept.enabled, 10):
                    logger.error(
                        "accept button is %s and %s"
                        % (
                            "exists" if accept.exists else "not exists",
                            "enabled" if accept.enabled else "not enabled",
                        )
                    )
                    return False
                if not accept.click_if_exists(timeout=5):
                    logger.error("accept error: button not exists")
                    return False
                time.sleep(2)
                return True

            def check_health():
                if self._wait(
                    lambda: handle_health_modal() or self.stop_check, 3 * 60, 5
                ):  # 没有健康授权之前，点不了
                    self.health_page_exists = False
                    self.allow_authorize(answer, "获取你的微信运动步数")
                # print("finish wait %f" % time.time())
                self.check_done = True
                self.health_modal_handle_thread = None

            self.stop_check = False
            self.check_done = False
            self.health_modal_handle_thread = threading.Thread(target=check_health)
            self.health_modal_handle_thread.setDaemon(True)
            self.health_modal_handle_thread.start()
        if not self._wait(lambda: self.health_page_exists, timeout=10, interval=2):
            # print("health_page_exists wait fail %f" % time.time())
            ret = self.allow_authorize(answer, "获取你的微信运动步数")
            return answer if ret else True
        else:
            # print("start wait %f" % time.time())
            # 出现了健康授权页，就必须得等授权页处理好——系统同意授权，但真正授权由微信授权弹窗确定
            ret = self._wait(lambda: not self.health_page_exists, 3 * 60, 10)
            return answer if ret else True

    def allow_record(self, answer=True):
        """
        处理录音确认弹框
        :param answer: True or False
        :return:
        """
        self.allow_authorize(answer, "使用你的麦克风")

    def allow_write_photos_album(self, answer=True):
        """
        处理保存相册确认弹框
        :param answer: True or False
        :return:
        """
        self.allow_authorize(answer, "保存图片或视频到你的相册")

    def allow_camera(self, answer=True):
        """
        处理使用摄像头确认弹框
        :param answer: True or False
        :return:
        """
        self.allow_authorize(answer, "使用你的摄像头")

    def allow_get_user_phone(self, answer=True):
        """
        处理获取用户手机号码确认弹框
        :param answer: True or False
        :return:
        """
        self.allow_authorize(answer, "你的手机号码")

    def allow_send_subscribe_message(self, answer=True):
        """
        允许发送订阅消息
        """
        if answer:
            btn_text = "允许|确定"
        else:
            btn_text = "取消"
        self.app.session(
            xpath=(
                '//StaticText[contains(@label, "以下消息")]/../../..//Button[contains("{btn_text}", @label)]'.format(
                    btn_text=btn_text
                )
            )
        ).click_if_exists(timeout=5.0)

    def modal_exists(self, title):
        """
        指定title的modal是否存在
        """
        if not self.app.session(
            xpath='//Button[.//StaticText[@name="{title}"]]'.format(title=title)
        ).exists:
            # title 和 content同时传入的时候，才能get到这个title的信息, 所以此处只有确定会有title时才做处理
            logger.info(f"没有出现预期弹窗: title[{title}]")
            return False
        return True

    def handle_modal(
        self, btn_text="确定", title: str = None, index=-1, force_title=False
    ):
        """
        处理模态弹窗
        :param title: 传入弹窗的 title 可以校验当前弹窗是否为预期弹窗
        :param btn_text: 根据传入的 文字 进行点击
        :param index: 当页面存在完全相同的两个控件时，通过指定 index 来选取
        :return:
        """
        if title and force_title:
            if not self.modal_exists(title):
                return False
        logger.info(f"可能出现弹框：{title}, 自动选择{btn_text}")
        return self.app.session(
            xpath='//Button//StaticText[@name="{btn_text}"]'.format(btn_text=btn_text),
            index=index,
        ).click_if_exists(timeout=5.0)

    def handle_action_sheet(self, item):
        """
        处理上拉菜单
        :param item: 要选择的 item
        :return:
        """
        self.app.session(class_name="ScrollView").subelems(
            class_name="Button", text=item
        ).click(timeout=10.0)

    def forward_miniprogram(
        self, name: str or list, text: str = None, create_new_chat: bool = True
    ):
        """
        通过右上角更多菜单转发小程序
        ps: 好友太多会有性能问题
        :type text: 分享携带的内容
        :param names: 要分享的人
        :param create_new_chat: 是否创建群聊
        :return:
        """
        self.app.session(class_name="Button", text="更多").click(timeout=10.0)
        if self.app.session(class_name="Button", partial_text="转发").exists:
            self.app.session(class_name="Button", partial_text="转发").click(timeout=10.0)
        elif self.app.session(class_name="Button", partial_text="发送").exists:
            self.app.session(class_name="Button", partial_text="发送").click(timeout=10.0)
        else:
            self.app.session(partial_text="关于").click(timeout=10.0)
            self.app.session(partial_text="推荐给朋友").click(timeout=10.0)

        return self.forward_miniprogram_inside(name, text, create_new_chat)

    def forward_miniprogram_inside(
        self, name: str or list, text: str = None, create_new_chat: bool = True
    ):
        """
        小程序内触发转发小程序
        ps: 好友太多会有性能问题
        :param names: 要分享的人
        :param create_new_chat: 是否创建群聊
        :return:
        """
        if self.app.session(
            xpath='//Button[.//StaticText[@name="分享提示"]]'
        ).exists:  # 开发版会弹出分享提示
            self.handle_modal("确定")

        if isinstance(name, str):
            name = [name]
        if len(name) > 1:  # 多于一个人是需要新建群
            create_new_chat = True
        if not create_new_chat and self.app.session(text="暂无最近聊天").exists:
            create_new_chat = True
        if create_new_chat:
            self.app.session(class_name="StaticText", text="创建新的聊天").click(timeout=10.0)
        for _name in name:
            self.app.session(
                class_name="TextField" if create_new_chat else "SearchField", text="搜索"
            ).set_text(_name)
            # count = 10
            time.sleep(1.5)  # 一定需要等待搜索出该用户
            self.app.session(
                class_name="StaticText", partial_text=_name, index=-1
            ).click(timeout=10.0)
            # count -= 1
        if create_new_chat:
            self.app.session(class_name="Button", partial_text="完成").click(timeout=10.0)
        self.app.session(class_name="Button", text="发送").click(timeout=10.0)

    def send_custom_message(self, message: str = None):
        """
        处理小程序 im 发送自定义消息
        :param message: 消息内容
        :return:
        """
        self.app.session(class_name="TextView").set_text(message + "\n")

    def phone_call(self):
        """
        处理小程序拨打电话
        :return:
        """
        self.app.session(partial_text="呼叫").click(timeout=10.0)
        self.app.session.alert.accept()

    def map_select_location(self, name: str = None):
        """
        原生地图组件选择位置
        :param name: 位置名称
        :return:
        """
        if not name:
            btn = self.app.session(class_name="Button", text="确定")
            if btn.exists and btn.enabled:
                return btn.click(timeout=10.0)
            else:
                return self.map_back_to_mp()
        self.app.session(class_name="SearchField", text="搜索地点").set_text(name)
        timeout = time.time() + 10
        while (
            self.app.session(text=name, class_name="StaticText").click_if_exists(
                timeout=5.0
            )
            and timeout > time.time()
        ):
            btn = self.app.session(class_name="Button", text="确定")
            if btn.exists and btn.enabled:
                return self.app.session(class_name="Button", text="确定").click(
                    timeout=10.0
                )
        # 没有命中就选第一个
        timeout = time.time() + 10
        while (
            self.app.session(xpath="//Table/Cell[1]").click_if_exists(timeout=5.0)
            and timeout > time.time()
        ):
            btn = self.app.session(class_name="Button", text="确定")
            if btn.exists and btn.enabled:
                return self.app.session(class_name="Button", text="确定").click(
                    timeout=10.0
                )

    def map_back_to_mp(self):
        """
        原生地图组件查看定位,返回小程序
        :return:
        """
        return self.app.session(class_name="Button", text="取消").click_if_exists(
            timeout=10.0
        )

    def deactivate(self, duration):
        """
        使微信进入后台一段时间, 再切回前台
        :param duration: float
        :return: NULL
        """
        self.app.deactivate(duration=duration)

    def click_coordinate(self, x, y):
        """
        点击坐标(x,y)
        :param x:
        :param y:
        :return:
        """
        self.app.session.click(x, y)

    def get_pay_value(self):
        """
        获取支付金额, IOS隐私设置不允许获取
        """
        raise NotImplementedError("iOS private value")

    def input_pay_password(self):
        """
        输入支付密码, IOS隐私设置不允许自动化输入
        """
        raise NotImplementedError()

    def close_payment_dialog(self):
        """
        关闭支付弹窗
        """
        self.app.session(text="closeModalBtn").click_if_exists(timeout=5.0)

    def hide_keyboard(self):
        """
        点击完成键，隐藏键盘
        :return:
        """
        self.app.session(class_name="Button", text="Done").click_if_exists(timeout=5.0)

    def text_exists(self, text="", iscontain=False, wait_seconds=5):
        """
        检测是否存在text
        """
        if iscontain:
            return self.app.session(partial_text=text).exists
        else:
            return self.app.session(text=text).exists

    def text_click(self, text="", iscontain=False):
        """
        点击内容为text的控件
        """
        if iscontain:
            return self.app.session(partial_text=text).click_if_exists(timeout=10.0)
        else:
            return self.app.session(text=text).click_if_exists(timeout=10.0)

    def is_app_in_foreground(self, appid):
        # exists window contains appid
        return self.app.session(class_name="Window", partial_text=appid).exists

    # back_to_miniprogram needed

    def _get_current_activity(self) -> str:
        """
        :return: PACKAGE/ACTIVITY
        """
        activity = []
        app_status = self.app.session.app_state(self.bundle_id)
        if app_status.value == AppState.RUNNING_IN_FOREGROUND.value:
            activity.append(self.bundle_id)
        else:
            activity.append(OTHER_PACKAGE)
        # 检查胶囊 和 webview，同时存在则在小程序中
        capsule = self.app.session(
            xpath='//Other/Button[@label="更多"]/following-sibling::XCUIElementTypeButton[@label="关闭"]'
        )
        webview = self.app.session(class_name="WebView")
        # 检查tabbar
        tabbar_items = ["微信", "通讯录", "发现", "我"]
        main_frame_tabbar = self.app.session(
            xpath='//TabBar/XCUIElementTypeButton[@label="%s"]/' % tabbar_items[0]
            + "/".join(
                'following-sibling::XCUIElementTypeButton[@label="%s"]' % item
                for item in tabbar_items[1:]
            )
        )
        if capsule.exists and webview.exists:
            activity.append(MINIPROGRAM_ACTIVITY)
        elif main_frame_tabbar.exists:
            activity.append(WECHAT_ACTIVITY)
        else:
            activity.append(OTHER_ACTIVITY)
        return "/".join(activity)

    def _is_in_wechat(self, activity: str):
        return activity.startswith(self.bundle_id)

    def _is_in_wechat_main(self, activity: str):
        return activity.endswith(WECHAT_ACTIVITY)

    def _is_in_miniprogram(self, activity: str):
        return activity.endswith(MINIPROGRAM_ACTIVITY)

    def _get_any_modal(self, confirm=False):
        """
        confirm == True: 确认/允许
        confirm == False: 拒绝/取消
        1. 授权弹窗 —— 拒绝/允许
        2. 分享弹窗 —— 发送
        3. 模态弹窗 —— 取消/确定
        4. ACTION SHEET暂不支持
        """
        auth = self.app.session(
            xpath='//Button[@label="授权说明"]/../Button[@name="{text}"]'.format(text="允许" if confirm else "拒绝")
        )
        share = self.app.session(
            xpath='//Image/StaticText[@name="发送给："]/following-sibling::XCUIElementTypeOther/Button[@label="发送"]'
        )
        modal = self.app.session(
            xpath='//Button[@label=""]/StaticText[contains("确定|取消", @label)]'
        )
        action_sheet = self.app.session(xpath='//ScrollView/Button[@label="取消"]')
        if auth.exists:
            return auth
        if modal.exists:
            return modal
        if action_sheet.exists:
            return action_sheet
        if share.exists:
            return share

    def _press_back(self):
        return self.app.press_back()

    @property
    def orientation(self):
        """
        获取屏幕方向
        :return:
        """
        return self.app.session.orientation

    @orientation.setter
    def orientation(self, value):
        """
        设置屏幕方向
        :param value: (string) LANDSCAPE | PORTRAIT | UIA_DEVICE_ORIENTATION_LANDSCAPERIGHT |
                    UIA_DEVICE_ORIENTATION_PORTRAIT_UPSIDEDOWN
        :return:
        """
        self.app.session.orientationset(value)

    def release(self):
        """
        remove port forward process
        :return:
        """
        self.release_auto_authorize()
        if self.perf_flag:
            self.stop_get_perf()
        self.wda_runner.remove_iproxy()

    ###############################
    #                      private                         #
    ###############################

    def _capture_photo(self, media_type, duration=10.0):
        """
        capture a photo by camera
        :param media_type: photo or video
        :param duration: capture duration
        :return:
        """
        if media_type == "photo":
            self.app.session(text="拍照").click(timeout=10.0)
            self.app.session(text="轻触拍照，按住摄像").click(timeout=10.0)
        elif media_type == "video":
            self.app.session(text="拍摄").click(timeout=10.0)
            self.app.session(text="轻触拍照，按住摄像").tap_hold(duration=duration)
        time.sleep(2.0)
        while self.app.session(text="确定").exists:
            try:
                self.app.session(text="确定").click(timeout=10.0)
            except Exception as e:
                logger.warning(str(e))

    def _select_photos_from_album(self, names: list, original=False):
        """
        select photos from album
        :param names: photo name list
        :param original: use original photo or not
        :return:
        """
        self.app.session(text="从手机相册选择").click(timeout=10.0)
        for name in names:
            rect = self.app.session(partial_text=name).bounds
            self.app.session.click(rect.x + rect.width - 10, rect.y + 10)
        if original:
            self.app.session(text="原图").click(timeout=10.0)
        self.app.session(partial_text="完成").click(timeout=10.0)

    def _select_video_from_album(self, name: str):
        """
        select video from album
        :param name: video file name
        :return:
        """
        self.app.session(text="从手机相册选择").click(timeout=10.0)
        rect = self.app.session(partial_text=name).bounds
        self.app.session.click(rect.x + rect.width - 10, rect.y + 10)
        self.app.session(partial_text="完成").click(timeout=10.0)

    def stop_wechat(self):
        """
        :return:
        """
        if self.health_modal_handle_thread:  # 健康弹窗仍在监听的话，需要断掉，不然会报错
            self.stop_check = True
            self._wait(lambda: self.check_done, timeout=20, interval=2)
        self.app and self.app.session.close()

    def get_authorize_settings(self):
        """
        todo @locker
        :return:
        """
        pass

    def back_from_authorize_setting(self):
        """
        todo @locker
        :return:
        """
        self.app.session(class_name="Button", text="返回").click(timeout=10.0)

    def authorize_page_checkbox_enable(self, name, enable):
        """
        todo @locker
        :return:
        """
        pass

    @staticmethod
    def _alert_callback(session):
        """
        auto accept when system alert view popup
        :return:
        """
        if session.alert.exists:
            logger.info("出现弹框, 默认接受")
            session.alert.accept()

    def _perf_callback(self, data_type: str, value: dict):
        # logger.debug(f"@_perf_callback {data_type}, {value}")
        if data_type not in ("cpu", "fps", "memory"):
            return
        timestamp = int(value["timestamp"] / 1000)  # value["timestamp"] is ms
        if len(self.perf_data) > 0 and self.perf_data[-1]["timestamp"] == timestamp:
            item = self.perf_data[-1]
        else:
            item = {"timestamp": timestamp}
            self.perf_data.append(item)
        if data_type == "cpu":
            item.update(
                {"mem": self.last_mem, "cpu": value["value"], "fps": self.last_fps}
            )
            self.last_cpu = value["value"]
        elif data_type == "fps":
            item.update(
                {"mem": self.last_mem, "cpu": self.last_cpu, "fps": value["value"]}
            )
            self.last_fps = value["value"]
        elif data_type == "memory":
            item.update(
                {"mem": value["value"], "cpu": self.last_cpu, "fps": self.last_fps}
            )
            self.last_mem = value["value"]

    def start_get_perf(self, timeinterval=15):
        """
        开始获取性能数据
        :param timeinterval: 抽样时间间隔
        :return: boolen
        """
        if self.perf_flag:
            return True
        global tidevice
        if not self.useTIDevice:
            return False
        if not tidevice:
            import tidevice
        t = tidevice.Device(self.udid)
        self.perf = tidevice.Performance(t)
        self.last_fps = 0
        self.last_cpu = 0
        self.last_mem = 0
        self.perf.start(self.bundle_id, callback=self._perf_callback)
        self.perf_flag = True
        return self.perf_flag

    def stop_get_perf(self):
        """
        停止获取性能数据
        :return: string: json.dumps([{cpu, mem, fps, timestamp}])
        """
        self.perf_flag = False
        if not self.perf:
            return ""
        self.perf.stop()
        result = json.dumps(self.perf_data)
        self.perf_data = []
        self.last_fps = 0
        self.last_cpu = 0
        self.last_mem = 0
        return result


if __name__ == "__main__":
    native = WXIOSNative(
        {
            "device_info": {
                # "udid": "aee531018e668ff1aadee0889f5ebe21a2292...",
                # "model": "iPhone XR",
                # "version": "12.2.5",
                # "name": "yopofeng's iPhone12"
            }
        }
    )
    native.start_wechat()
    try:
        native.pick_media_file(names=["照片6,拍摄时间,2021年3月22日 上午11:49"])
    finally:
        native.release()
