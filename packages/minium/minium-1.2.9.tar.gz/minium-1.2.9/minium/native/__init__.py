#!/usr/bin/env python3
# Created by xiazeng on 2019-05-22
import os.path
import sys
import typing

work_root = os.path.abspath(os.path.dirname(__file__))
lib_path = os.path.join(work_root, "lib")
sys.path.insert(0, lib_path)

from minium.framework.miniconfig import MiniConfig, logger
from .exception import *

# # weChat
from minium.native.wx_native.basenative import BaseNative

# from minium.native.wx_native.androidnative import WXAndroidNative
# from minium.native.wx_native.iosnative import WXIOSNative
# from minium.native.wx_native.idenative import IdeNative

# # QQ
# from minium.native.qq_native.qandroidnative import QAndroidNative
# from minium.native.qq_native.qiosnative import QiOSNative

# platform
from minium.utils.platforms import *
# OS_ANDROID = "android"
# OS_IOS = "ios"
# OS_IDE = "ide"
# OS_MAC = "mac"
# OS_WIN = "win"

# application
APP_WX = "wx"
APP_QQ = "qq"


class APPS(dict):
    def __getitem__(self, __k):
        try:
            v = super().__getitem__(__k)
        except KeyError:
            v = None
        if v is not None:
            return v
        if __k == "wx_android":
            from minium.native.wx_native.androidnative import WXAndroidNative

            super().__setitem__(__k, WXAndroidNative)
            return WXAndroidNative
        elif __k == "wx_ios":
            from minium.native.wx_native.iosnative import WXIOSNative

            super().__setitem__(__k, WXIOSNative)
            return WXIOSNative
        elif __k == "ide":
            from minium.native.wx_native.idenative import IdeNative

            super().__setitem__(__k, IdeNative)
            return IdeNative
        elif __k == "qq_android":
            from minium.native.qq_native.qandroidnative import QAndroidNative

            super().__setitem__(__k, QAndroidNative)
            return QAndroidNative
        elif __k == "qq_ios":
            from minium.native.qq_native.qiosnative import QiOSNative

            super().__setitem__(__k, QiOSNative)
            return QiOSNative
        raise KeyError("APPS not support %s" % __k)


APP = APPS()


def get_native_driver(os_name, conf):
    if os_name.lower() not in [OS_ANDROID, OS_IDE, OS_IOS]:
        raise RuntimeError("the 'os_name' in your config file is not in predefine")
    if os_name.lower() != OS_IDE and conf.get("app", None) not in [APP_WX, APP_QQ]:
        raise RuntimeError(
            f"the 'app': '{os_name}' in your config file is not in predefine, not support yet"
        )
    if os_name.lower() == OS_IDE:
        return APP[os_name.lower()]({})
    elif conf.device_desire is None:
        logger.warning(
            "your platform is [{}], but dosn't configure the [device_desire] field, native"
            " interface will not in use!".format(os_name)
        )
        return APP[OS_IDE]({})
    else:
        json_conf = {"outputs": conf.outputs}
        json_conf.update(conf.device_desire or {})
        return APP[conf.app.lower() + "_" + os_name.lower()](json_conf)


def Native(json_conf, platform=None, app="wx"):
    cfg = MiniConfig({"platform": platform, "app": app, "device_desire": json_conf})
    return get_native_driver(platform, cfg)
