#!/usr/bin/env python3
# Created by xiazeng on 2019-06-11
from .basenative import BaseNative, NativeError


class IdeNative(BaseNative):
    mini = None  # ide的native操作也以来minium的实例，可能引起循环引用，需要谨慎处理

    def __del__(self):
        self.mini = None

    def release(self):
        self.release_auto_authorize()
        self.mini = None

    def start_wechat(self):
        ...

    def stop_wechat(self):
        ...

    def connect_weapp(self, path):
        ...

    def screen_shot(self, filename, return_format="raw"):
        if self.mini:
            self.mini.app.platform = "ide"  # 防止无限回调
            self.mini.app.screen_shot(filename, return_format)
            return filename
        return ""

    def pick_media_file(
        self,
        cap_type="camera",
        media_type="photo",
        original=False,
        duration=5.0,
        names=None,
    ):
        raise NotImplementedError("ide not implemented")

    def allow_authorize(self, answer=True, title=None):
        self._allow_authorize(answer)

    def _allow_authorize(self, answer):
        """
        mock实现, 所有接口引发的原生弹窗授权理论上都可以使用
        """
        if self.mini:
            return self.mini.app._evaluate_js(
                "ideHandleAuthModal",
                [
                    "允许" if answer else "拒绝",
                ],
            )
        return False

    def allow_login(self, answer=True):
        self._allow_authorize(answer)

    def allow_get_user_info(self, answer=True):
        self._allow_authorize(answer)

    def allow_get_location(self, answer=True):
        self._allow_authorize(answer)

    def allow_get_we_run_data(self, answer=True):
        self._allow_authorize(answer)

    def allow_record(self, answer=True):
        self._allow_authorize(answer)

    def allow_write_photos_album(self, answer=True):
        self._allow_authorize(answer)

    def allow_camera(self, answer=True):
        self._allow_authorize(answer)

    def allow_get_user_phone(self, answer=True):
        self._allow_authorize(answer)

    def allow_send_subscribe_message(self, answer=True):
        """
        允许发送订阅消息
        """
        if self.mini:
            return self.mini.app._evaluate_js(
                "ideHandleAuthModal",
                [
                    "允许" if answer else "取消",
                ],
            )
        return False

    def handle_modal(self, btn_text="确定", title: str = None, force_title=False):
        """
        mock实现, 所有接口引发的原生弹窗理论上都可以使用
        ps: 需要兼容一下授权弹窗
        """
        if self.mini:
            return self.mini.app._evaluate_js(
                "ideHandleModal",
                [
                    btn_text,
                ],
            )

    def handle_action_sheet(self, item):
        self.handle_modal(item)

    def forward_miniprogram(
        self, name: str, text: str = None, create_new_chat: bool = True
    ):
        raise NotImplementedError("ide not implemented")

    def forward_miniprogram_inside(
        self, name: str, text: str = None, create_new_chat: bool = True
    ):
        raise NotImplementedError("ide not implemented")

    def input_text(self, text):
        if self.mini:
            self.mini.app.get_current_page().get_element("input").input(text)

    def input_clear(self):
        if self.mini:
            self.mini.app.get_current_page().get_element("input").input("")

    def textarea_text(self, text, index=0):
        if self.mini:
            els = self.mini.app.get_current_page().get_elements("textarea")
            els[index].input(text)

    def textarea_clear(self, index=0):
        if self.mini:
            els = self.mini.app.get_current_page().get_elements("textarea")
            els[index].input("")

    def send_custom_message(self, message=None):
        ...

    def phone_call(self):
        ...

    def map_select_location(self, name=None):
        if self.mini:
            return self.mini.app._evaluate_js(
                "ideHandleMap",
                [
                    name,
                ],
            )

    def map_back_to_mp(self):
        if self.mini:
            return self.mini.app._evaluate_js(
                "ideHandleMap",
                [
                    "取消",
                ],
            )

    def deactivate(self, duration):
        ...

    def get_authorize_settings(self):
        ...

    def back_from_authorize_setting(self):
        ...

    def authorize_page_checkbox_enable(self, name, enable):
        ...
