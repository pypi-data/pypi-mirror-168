#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
Author:         lockerzhang
Filename:       connection_new.py
Create time:    2019/6/14 16:29
Description:

"""
import re
import time
import websocket
import json
from .minium_log import MonitorMetaClass
from minium.framework.exception import *
from uuid import uuid4
import threading
import logging

CLOSE_TIMEOUT = 5
MAX_WAIT_TIMEOUT = 30
g_thread = None
logger = logging.getLogger("minium")


class DevToolMessage(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise MiniNotAttributeError(name)


class Command(object):
    max_timeout = 30
    """
    通信命令
    :method: 命令方法
    :params: 命令参数
    :timeout: 命令返回时间，仅对同步指令有效
    :desc: 命令超时时提醒信息
    """

    def __init__(
        self, method: str, params: dict = None, max_timeout: int = None, desc: str = None
    ) -> None:
        self.id = None
        self.method = method
        self.params = params or {}
        self.max_timeout = max_timeout or self.max_timeout
        self.desc = desc or f"call {method}"

    @classmethod
    def set_timeout(cls, timeout):
        cls.max_timeout = timeout


def json2obj(data):
    try:
        return json.loads(data, object_hook=DevToolMessage)
    except (TypeError, json.JSONDecodeError):
        return None


class Connection(object, metaclass=MonitorMetaClass):
    def __init__(self, uri, timeout=MAX_WAIT_TIMEOUT):
        super().__init__()
        self.logger = logger
        self.observers = {}
        self.uri = uri
        self.timeout = timeout
        Command.set_timeout(self.timeout)
        self._is_connected = False
        self._msg_lock = threading.Condition()
        self._ws_event_queue = dict()
        self._req_id_counter = int(time.time() * 1000) % 10000000000
        self._sync_wait_map = {}
        self._async_msg_map = {}
        self._method_wait_map = {}
        self._client = websocket.WebSocketApp(
            self.uri,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
        )
        self._connect()

    def register(self, method: str, callback):
        if method not in self.observers:
            self.observers[method] = []
        self.observers[method].append(callback)

    def remove(self, method: str, callback=None):
        if method in self.observers.keys():
            if callback is None:  # remove all callback
                del self.observers[method]
            elif callback in self.observers[method]:
                self.observers[method].remove(callback)
        else:
            self.logger.warning("remove key which is not in observers")

    def remove_all_observers(self):
        try:
            obs_list = [x for x in self.observers.keys()]
            for obs in obs_list:
                del self.observers[obs]
        except Exception as e:
            raise KeyError(e)

    def notify(self, method: str, message):
        if method == "App.bindingCalled" and message["name"] in self.observers:
            for callback in self.observers[message["name"]]:
                if callable(callback):
                    callback(message)
                else:
                    raise MiniNoncallableError(f"{str(callback)}(message={message})")
            return
        elif method in self.observers:
            for callback in self.observers[method]:
                if callable(callback):
                    callback(message)
                else:
                    raise MiniNoncallableError(f"{str(callback)}(message={message})")
        else:
            return

    def _connect(self, timeout=30):

        self._thread = threading.Thread(target=self._ws_run_forever, args=())
        self._thread.daemon = True
        self._thread.start()

        s = time.time()
        while time.time() - s < timeout:
            if self._is_connected:
                logger.info("connect to WebChatTools successfully")
                break
        else:
            raise MiniTimeoutError(
                "connect to server timeout: %s, thread:%s" % (self.uri, self._thread.is_alive())
            )

    def _ws_run_forever(self):
        try:
            self._client.run_forever()
        except Exception as e:
            self.logger.exception(e)
            self._is_connected = False
            return
        self.logger.info("websocket run forever shutdown")

    def _send(self, message):
        return self._client.send(message)

    def _wait(self, cmd: Command):
        stime = time.time()
        self._msg_lock.acquire()
        self._msg_lock.wait(cmd.max_timeout)  # 如果是因为其他命令的返回触发了notify，需要重新等待
        self._msg_lock.release()
        etime = time.time()
        if etime - stime >= cmd.max_timeout:
            cmd.max_timeout = 0
        else:
            cmd.max_timeout = cmd.max_timeout - (etime - stime)  # 剩余要等待的时间

    def _notify(self):
        self._msg_lock.acquire()
        self._msg_lock.notify_all()  # 全部唤醒，让其自己决定是否需要重新wait
        self._msg_lock.release()

    def send(self, method: str or Command, params=None, max_timeout=None):
        # 同步发送消息，函数会阻塞
        if isinstance(method, Command):
            cmd = method
        else:
            cmd = Command(method, params, max_timeout)
        cmd.id = str(uuid4())
        message = json.dumps(
            {"id": cmd.id, "method": cmd.method, "params": cmd.params}, separators=(",", ":")
        )
        self._sync_wait_map[cmd.id] = None  # 该ID未有返回message
        self.logger.debug("SEND > %s" % message)
        self._send(message)
        return self._receive_response(cmd)

    def send_async(self, method, params=None) -> str:
        if not params:
            params = {}
        uid = uuid4()
        message = json.dumps({"id": str(uid), "method": method, "params": params})
        self._client.send(message)
        self.logger.debug("ASYNC_SEND > %s" % message)
        return str(uid)

    def _receive_response(self, cmd: Command):
        # 等待接收到message的通知
        while cmd.max_timeout > 0:
            self._wait(cmd)

            if cmd.id in self._sync_wait_map and self._sync_wait_map[cmd.id] is not None:  # 获取到了数据
                response = self._sync_wait_map.pop(cmd.id)
                if "error" in response and "message" in response["error"]:
                    err_msg = response["error"]["message"]
                    if err_msg:
                        self.logger.error(f"[{cmd.id}]: {err_msg}")
                        if err_msg.find("unimplemented") > 0:
                            self.logger.warn(f"{err_msg}, It may be caused by the low sdk version")
                        raise MiniAppError(err_msg)
                return response
            elif cmd.max_timeout > 0:  # 线程是被其他消息唤醒，重新等待
                self.logger.debug("rewait for %s" % cmd.id)
                continue
            else:
                if cmd.id in self._sync_wait_map:
                    del self._sync_wait_map[cmd.id]
                raise MiniTimeoutError(
                    "[%s] receive from remote timeout, id: %s" % (cmd.desc, cmd.id)
                )

    def _on_close(self, *args):
        self._is_connected = False

    def _on_open(self, *args):
        self._is_connected = True

    def _on_message(self, message, *args):
        # 有些ws的库会传ws实例！至今不懂为什么有些会有些不会，先兼容一下
        if args:
            # 会传 ws 实例的情况
            message = args[0]
        if len(message) > 512:
            self.logger.debug("RECV < %s..." % message[:509])
        else:
            self.logger.debug("RECV < %s" % message)
        ret_json = json2obj(message)
        if isinstance(ret_json, dict):
            if "id" in ret_json:  # response
                req_id = ret_json["id"]
                if req_id in self._sync_wait_map:
                    self._sync_wait_map[req_id] = ret_json
                    self._notify()
                else:
                    self.logger.warning("received async msg: %s", req_id)
                    self._async_msg_map[req_id] = ret_json
            else:
                if "method" in ret_json and ret_json["method"] in self._method_wait_map:
                    self._method_wait_map[ret_json["method"]] = ret_json
                    self._notify()

                if "method" in ret_json and "params" in ret_json:
                    # self._push_event(ret_json["method"], ret_json["params"])
                    self.notify(ret_json["method"], ret_json["params"])

    def _push_event(self, method, params):
        if method in self._ws_event_queue:
            self._ws_event_queue[method].append(params)
        else:
            self._ws_event_queue[method] = [params]

    def _on_error(self, error, *args):
        if args:
            # 会传 ws 实例的情况
            error = args[0]
        if "Connection is already closed" in str(error):
            self.logger.warning(error)
            return
        self.logger.error(error)
        self._is_connected = False

    def destroy(self):
        logger.error("断开连接")
        self._client.close()
        self._thread.join(CLOSE_TIMEOUT)

    def wait_for(self, method: str or Command, max_timeout=None):
        if isinstance(method, Command):
            cmd = method
        else:
            cmd = Command(method, max_timeout=max_timeout)
        if cmd.method in self._method_wait_map and self._method_wait_map.get(
            cmd.method, None
        ):  # 已经有间听到并没被删除（一般只有别的线程同样在等这个方法，但又还没响应才会命中，兜底逻辑）
            return True
        self._method_wait_map[cmd.method] = None
        while cmd.max_timeout > 0:
            self._wait(cmd)
            if cmd.method in self._method_wait_map and self._method_wait_map.get(cmd.method, None):
                del self._method_wait_map[cmd.method]
                return True
        self.logger.error("Can't wait until %s" % cmd.method)
        return False

    def get_aysnc_msg_return(self, msg_id=None):
        if not msg_id:
            self.logger.warning(
                "Can't get msg without msg_id, you can get msg_id when calling send_async()"
            )
        if msg_id in self._async_msg_map:
            return self._async_msg_map.pop(msg_id)
        return None
