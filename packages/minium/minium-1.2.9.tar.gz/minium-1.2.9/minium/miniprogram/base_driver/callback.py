"""
callback类, 供hook等需要callback的场景使用
"""
import types
import typing
import threading

class Callback(object):
    def __init__(self, callback: types.FunctionType = None) -> None:
        self.__callback = callback
        self.__called = threading.Semaphore(0)
        self.__is_called = False
        self.__callback_result = None

    def callback(self, args):
        self.__is_called = True
        self.__callback_result = args[0] if args and len(args) == 1 else args
        self.__called.release()
        if self.__callback:
            self.__callback(*args)

    @property
    def is_called(self):
        return self.__is_called

    def wait_called(self, timeout=10) -> bool:
        """
        等待回调调用, 默认等待最多10s
        """
        if self.__is_called:
            return True
        return self.__called.acquire(timeout=timeout)

    def get_callback_result(self, timeout=0) -> any:
        """
        获取回调结果, 超时未获取到结果报AssertionError
        1. 回调参数只有一个的情况会解构
        2. 回调参数中有多个的情况会直接返回参数list
        """
        if self.wait_called(timeout):
            return self.__callback_result
        assert self.__is_called, f"No callback received within {timeout} seconds"
